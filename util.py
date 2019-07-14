import re
import os
import urllib2
from page_parser import *
from run import *

def get_title_url():
    map_word=read_keywords()
    list_word=[]
    file_name_list=[]
    for key in map_word.keys():
        file_name_list.append(key)
        list_word.append(map_word[key])

    file=open('save_title_url','a+')

    for i in range(0,len(list_word)):
        url=list_word[i]
        total_page_number=get_total_page(url)

        if total_page_number==1:
            # articles=parse.get_meta_article(url)
            title,link=get_title_link1(url)

            for i in range(0,len(title)):
                file.write(title[i]+"^"+link[i]+"\n")

                # print title[i],link[i]

        else:
            for page in range(1,total_page_number+1):
                end_page=url.find("&page=")
                url=url[0:end_page+6]+str(page)
                title,link=get_title_link1(url)

                for i in range(0,len(title)):
                    file.write(title[i]+"^"+link[i]+"\n")
                    # print title[i],link[i]

    file.close()

    print 'Completed!'
