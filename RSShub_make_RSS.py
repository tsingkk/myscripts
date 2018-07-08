#!/usr/bin/env python

import re

RRShub_site = "http:// rsshub.app/"

weburl = []
while True:
    w = input('输入订阅网页网址(含http,输入0结束)：')
    if w == '0':
        break
    weburl.append(w)

pattern = {'jike_jingxuan':
           re.compile('web.okjike.com/topic/[A-Za-z0-9]+/official'),
           'jianshu_user':
           re.compile('www.jianshu.com/u/[A-Za-z0-9]+'),
           'jianshu_collection':
           re.compile('www.jianshu.com/c/[A-Za-z0-9]+'),
           'bilibili_bangumi':
           re.compile('www.bilibili.com/bangumi/play/ep[A-Za-z0-9]+'),
           'bilibili_user_video':
           re.compile('space.bilibili.com/[A-Za-z0-9]+/#/video')
           }


def jike_jingxuan_s(web):
    return web.split('/')[4]


def jianshu_user_s(web):
    return web.split('/')[4]


def jianshu_collection_s(web):
    return web.split('/')[4].split('?')[0]


def bilibili_bangumi_s(web):
    return web.split('/')[5][2:]


def bilibili_user_video_s(web):
    return web.split('/')[3]


web_extract = {'jianshu_user': jianshu_user_s,
               'jike_jingxuan': jike_jingxuan_s,
               'jianshu_collection': jianshu_collection_s,
               'bilibili_bangumi': bilibili_bangumi_s,
               'bilibili_user_video': bilibili_user_video_s,
               }

routing = {'jike_jingxuan': "jike/topic/",
           'jianshu_user': "jianshu/user/",
           'jianshu_collection': 'jianshu/collection/',
           'bilibili_bangumi': 'bilibili/bangumi/',
           'bilibili_user_video': 'bilibili/user/video/',
           }

for i in range(len(weburl)):
    for j in pattern.keys():
        m = re.search(pattern[j], weburl[i])
        if m:
            break
    print(j, '=>', RRShub_site + routing[j] + web_extract[j](weburl[i]))
