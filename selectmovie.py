#!/usr/bin/env python

#select random one of movies in my disk


def getmovieslist(findpath,flagstr):
	import os
	movielist=[]
	movienames=[]
	for root,dirs,files in os.walk(findpath):
		for dnames in dirs:
			subnames=os.path.join(root,dnames)
			movienames.extend(os.listdir(subnames))
		for fnames in files:
			movienames.extend(fnames)
	if (len(movienames)>0):
		for mn in movienames:
			if (len(flagstr)>0):
				if os.path.splitext(mn)[1] in flagstr:
					fullmoviename=os.path.join(findpath,mn)
					movielist.append(fullmoviename)
			else:
				fullmoviename=os.path.join(findpath,mn)
				movielist.append(fullmoviename)
	return movielist

flag=['.mkv','.rmvb','.mp4','.avi']
path=['/media/kkk/MEDIA/eyes faver/电影','/media/kkk/MEDIA/迅雷下载','/media/kkk/SOFTWARE/迅雷下载','/media/kkk/NOWINDOWS']
allmovielist=[]
for pt in path:
	ls=getmovieslist(pt,flag)
	allmovielist.extend(ls)
from random import choice
print(choice(allmovielist))
