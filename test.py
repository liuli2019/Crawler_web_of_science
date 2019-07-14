import re
import os
import urllib2
from page_parser import *
from run import *

s=None

def fun():
    global s
    s="HKK"
def t():
    global s
    # s=s+'ol'
    print s

def get_all_data():
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
                print title[i],link[i]

            # articles_urls=get_title_link(url)
            # for u in articles_urls:
            #     print parse_article_title(u),u
        else:
            for page in range(1,total_page_number+1):
                end_page=url.find("&page=")
                url=url[0:end_page+6]+str(page)
                title,link=get_title_link1(url)

                for i in range(0,len(title)):
                    file.write(title[i]+"^"+link[i]+"\n")
                    print title[i],link[i]

                # articles_urls=get_title_link(url)
                #
                # for u in articles_urls:
                #     print parse_article_title(u),u
    file.close()

    print 'Completed!'

def get_none():
    f=open('summary')
    title_none=[]
    content={}
    for line in f.readlines():
        s=line.split('^')[3]
        if s.strip('\n')=='None':
            title_none.append(line.split('^')[0])

    file=open('save_title_url')

    for line in file.readlines():
        # print type(line)
        t=line.split('^')
        if len(t)==2:
            content[t[0]]=t[1]
            # content[line.split('^')[0]]=line.split('^')[1]


    f.close()
    file.close()

    # print len(title_none)
    t=open('abst','a+')
    n=1

    for title in title_none:
        if title not in content.keys():
            print 'Not found'
            continue
        url=content[title]
        abstract=parse_article_abstract(url)
        print n,'/',len(title_none)
        if abstract is None:
            print title,url
            abstract='None'
        t.write(title+'^'+abstract+'\n')
        n=n+1
        # print title,'^',abstract


def main():

    # get_title_link(url)
    # get_all_data()
    # get_none()
    # url="http://apps.webofknowledge.com/full_record.do?product=UA&search_mode=GeneralSearch&qid=1&SID=8BXxqC2RXciQAsyBo1b&page=1&doc=1"
    # url='http://apps.webofknowledge.com/CitedFullRecord.do?product=UA&colName=WOS&SID=8BXxqC2RXciQAsyBo1b&search_mode=CitedFullRecord&isickref=WOS:000246347900046&cacheurlFromRightClick=no'
    # print parse_article_abstract(url)
    # url="http://apps.webofknowledge.com/Search.do?product=UA&SID=7AVMofJ8oHZBN7HNQUi&search_mode=GeneralSearch&prID=af6f103f-afcb-4850-a395-e0c0213f0f88"
    # get_title_link1(url)
    fun()
    t()

if __name__ == '__main__':
    main()
