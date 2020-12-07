# -*- coding: utf-8 -*-
import boto3
import json
import urllib.request
from urllib import parse
from bs4 import BeautifulSoup

def lambda_handler(event, context):

    s3_client = boto3.client('s3')
    response = event['body']
    response = json.loads(response)
    response = response['text']
    result_list = []
    if response == "":
        result_list.append("단어를 입력하세요!")
    else:
        word = parse.quote(response)
        url = f"https://dict.naver.com/search.nhn?dicQuery={word}\&query={word}\&target=dic\&ie=utf8\&query_utf=\&isOnlyViewEE="
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
        a = soup.select_one("#content > div")
    
        if str(a['class']) == "['search_result']":
            result_list.append("없는 단어입니다.")
        elif str(a['class']) == "['kr_dic_section', 'search_result', 'dic_kr_entry']":
            find_word = a.select_one("ul > li> p > a > span.c_b > strong")
            result_list.append(find_word.text)
            mean = a.select("ul > li> p")[1].text
            mean = " ".join(mean.split())
            result_list.append(mean)    
        else:
            find_word = a.select_one("dl > dt > a > span.c_b > strong")
            result_list.append(find_word.text)
            mean = a.select_one("dl > dd").text
            mean = " ".join(mean.split())
            result_list.append(mean)
    return {
        'statusCode' : 200,
        'headers' : {
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Credentials" : 1
        },
        'body' : json.dumps(result_list, ensure_ascii=False)
    }
