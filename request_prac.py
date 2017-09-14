import requests
import urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

ACCESS_TOKEN="3079138173.053597e.3991399879fe43cc979404801981e6ff"
BASE_URL="https://api.instagram.com/v1/"

def delete_negative_comment(insta_username):
    posts_data = get_user_posts(insta_username)
    posts_data = posts_data[0]
    media_id=posts_data["id"]
    url=(BASE_URL + "media/%s/comment/?access_tokrn=%s")%(media_id,ACCESS_TOKEN)
    comment_info=requests.get(url).json()
    blob=TextBlob(comment_info["text"], analyzer= NaiveBayesAnalyzer())
    return blob

def get_data_from_url(url):
    r=requests.get(url)
    return r.json()['data']

def self_info():
    url= BASE_URL + "users/self/?access_token=%s"%ACCESS_TOKEN
    print 'GET request url : %s' % (url)
    user_info=requests.get(url).json()

    if user_info['meta']['code']==200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are folowing : %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'
def get_user_id(insta_username):
    request_url= BASE_URL + "users/search/?q=%s&access_token=%s"%(insta_username,ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info=requests.get(request_url).json()['data']
    return user_info
def get_user_info(user_name):
    user_id=get_user_id(user_name)
    if user_id==None:
        print 'User does not exist'
        exit();
    url = BASE_URL + "users/%s?access_token=%s" % (user_id,ACCESS_TOKEN)
    print 'GET request url : %s' % (url)
    user_info=requests.get(url).json()
    if user_info['meta']['code']==200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are folowing : %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'
def download_image(item):
    urllib.urlretrieve(item['url'],item['name'])
def get_own_posts():
    url = BASE_URL + "users/self/media/recent?access_token=%s" %  ACCESS_TOKEN
    posts_info=requests.get(url).json()['data']
    images=[]
    for e in posts_info:
        images.append({
            'url' : e['images']['standard_resolution']['url'],
            'name' : e['id'] + ".jpeg"
        })

    for e in images:
        download_image(e)
def get_user_posts(insta_username):
    user_info=get_user_id(insta_username)
    url = BASE_URL + "users/%s/media/recent?access_token=%s" % (user_info,ACCESS_TOKEN)
    posts_info = get_data_from_url(url)
    return posts_info

def like_a_post(username):
    posts_data=get_user_posts(username)
    posts_data=posts_data[0]
    url=BASE_URL + "media/%s/likes=" % (posts_data["id"])
    params={
        "access_token": ACCESS_TOKEN
    }
    r=requests.post(url,params).json()
    data=r['data']
    return data

def comment_on_post(post_id):
    url= BASE_URL + "media/%s/comments="%post_id
    params={
        "access_token": ACCESS_TOKEN,
        "text": "Testing Using Instabot"
    }
    r=requests.post(url,params)
    return r