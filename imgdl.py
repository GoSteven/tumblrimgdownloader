#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib2
from os.path import basename
from urlparse import urlsplit
import os
from pprint import pprint
from threading import Thread
from Queue import Queue
import time
import sys
# Universal Feed Parser(http://www.crummy.com/software/BeautifulSoup/)
import feedparser
# BeautifulSoup(http://www.crummy.com/software/BeautifulSoup/)
from BeautifulSoup import BeautifulSoup

time1 = time.time()

#try:
##  rss 
#feed_ = feedparser.parse(sys.argv[2])
## 
#count = len(feed_['entries'])
#counts = [i for i in range(count)]
#
#
##  description 
#descriptions = [feed_.entries[x].description for x in counts]
#description_soup = BeautifulSoup(''.join(descriptions))
##  descriptions  img  src 
#imgs_src = [description_soup.findAll('img')[x]['src'] for x in counts]
#

####tumblr api
imgs_src = []
for i in range (0,int(sys.argv[3])):
    url=sys.argv[2] + "/api/read?start=" + str(i*20)
    soup = BeautifulSoup(urllib2.urlopen(url))
    count = len(soup.findAll('photo-url'))
    counts = [i for i in range(count)]
    imgs_src += [soup.findAll('photo-url')[x].contents[0] for x in counts]


#print soup.findAll('photo-url')['max-width']
print len    

#except:
#    print 'RSS Error! please check!'
    # 
#    exit()

# 
save_path = 'imgs'
# 
if not os.path.exists(save_path):
    # 
    os.makedirs(save_path)

# 

q = Queue()

def download_img(img_src, savePath):
    try:
        if not "500" in img_src:
            return;
        imgData = urllib2.urlopen(img_src).read()
        # 
        fileName = save_path + '\\' + basename(urlsplit(img_src)[2])
        # 
        if not os.path.exists(fileName):
            output = open(fileName,'wb+')
            output.write(imgData)
            output.close()
            print "Finished download %s\n" %img_src
    except:
        print "Download %s failed\n" %img_src

def worker():
    while True:
        download_img(q.get(), save_path)
        q.task_done()

def download_imgs(imgs_src, save_path, num_workers):
    for i in range(num_workers):
        t = Thread(target=worker)
        t.setDaemon(True)
        t.start()
    # 
    for img_src in imgs_src:
        q.put(img_src, save_path)
    q.join()

def process(imgs_src, save_path, numthreads):
    if numthreads > 1:
        download_imgs(imgs_src, save_path, numthreads)
    else:
        for img_src in imgs_src:
            try:
                if not "500" in img_src:
                    return;
                imgData = urllib2.urlopen(img_src).read()
                # 
                fileName = save_path + '\\' + basename(urlsplit(img_src)[2])
                # 
                if not os.path.exists(fileName):
                    output = open(fileName,'wb+')
                    output.write(imgData)
                    output.close()
                    print "Finished download %s\n" %img_src
            except:
                print "Download %s failed\n" %img_src

if __name__ == '__main__':
    process(imgs_src, save_path, int(sys.argv[1]))
    time2 = time.time()
    print time2 - time1
