from django.http import JsonResponse, response
from django.shortcuts import render
import requests,json,asyncio
from bs4 import BeautifulSoup


# this is for get available data and api methods
keys_info = ["biography","external_url","external_url_linkshimmed","edge_followed_by"
                  ,"edge_follow","full_name","highlight_reel_count","id","is_business_account",
                  "is_professional_account","is_embeds_disabled","is_joined_recently","business_email"
                  ,"business_category_name","category_name","is_private","is_verified","profile_pic_url"
                  ,"username","edge_felix_video_timeline","edge_owner_to_timeline_media",
                  "edge_media_collections"]

INSTA_API_METHODS = new_keys_info = ["biography","page_url","page_url_linkshimmed","followers","following",
                           "full_name","highlight_reel_count","id_number","is_business_account","is_professional_account"
                           ,"is_embeds_disabled","is_joined_recently","business_email","business_category_name","category_name",
                           "is_private","is_verified","profile_pic_url","username","posts_video","posts_count",
                           "edge_media_collections"]

TWITTER_API_METHODS = ["Name","Bio","Location","Retweets","URL","Followers","Following"]

def insta_api():
       url = "https://instagram28.p.rapidapi.com/user_info"
       new_data_info = {}
       querystring = {"user_name":"feg_token"}
       headers = {
           'x-rapidapi-host': "instagram28.p.rapidapi.com",
           'x-rapidapi-key': "rapid-key"
           }
       data = requests.request("GET", url, headers=headers, params=querystring)
       print("-"*20 + "req sent!" + "-"*20)
       data_info = json.loads(data.text)

       if len(data_info) > 1:
           with open('json_data.json', 'w') as outfile:
                   json.dump(data_info, outfile)  
       else: 
            with open('json_data.json', 'r') as outfile:
                data_info = json.load(outfile)
       
       for num,key in enumerate(keys_info,len(keys_info)):
           print(num,key)
           new_data_info[new_keys_info[num-22]] = data_info["data"]["user"][key]

       return new_data_info

def twitter_api():

    req = requests.get("https://foller.me/fegtoken")
    soup = BeautifulSoup(req.text, 'html.parser')

    if "FEG" not in soup.title.text:
        with open("twitter-data.txt","r") as data_page:
                soup = BeautifulSoup(data_page, 'html.parser')
    else:
       with open("twitter-data.txt","w") as data_page:
               data_page.write(req.text)
               data_page.close()

    css_objects = soup.select("[class~=condensed-table]")
    data,twitter_data = (dict(),dict())

    for count in  range(len(css_objects)):
         b = soup.select("[class~=condensed-table]")[count]
         for num,key in enumerate(b.select("td"),0):
             data[num] = (key.text).strip("\n").replace("\t","")
        # for every count in new list (sort list)
         for num_2 in range(len(data)):
               if num_2 % 2 == 0:
                  twitter_data[data[num_2]] = data[num_2+1]
                  
    return twitter_data

# Create your views here.
def insta_get_data(request,slug):
    if slug == "get_data":
       data = insta_api()
    else:
        for method in INSTA_API_METHODS:
             if slug == method:
                data = insta_api()[method]
    
    return JsonResponse(data,safe=False)

def twitter_get_data(request,slug):
    # for method in aoi
    try:
       if slug == "get_data":
          data = twitter_api()
       else:
          for method in TWITTER_API_METHODS:
                if slug == method:
                   data = twitter_api()[method]
    except:
        data = {
            "title":"Error",
            "description":"Page not found!"
        }
    return JsonResponse(data,safe=False)
