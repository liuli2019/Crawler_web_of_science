# -*- coding: utf-8 -*-
import  re
import urllib2

headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/51.0.2704.103 Safari/537.36"}
html=None

def init(url):
    global html
    req=urllib2.Request(url,headers=headers)
    response=urllib2.urlopen(req)
    html=response.read()

def get_title_link1(url):
    req=urllib2.Request(url,headers=headers)
    response=urllib2.urlopen(req)
    html=response.read()
    pattern =re.compile(ur'<span class="smallV110"></span><a class="smallV110 snowplow-full-record"(.+?)\n<value lang_id="">')
    s=pattern.finditer(html)
    link_list=[]
    for item in s:
        content=item.group()
        index_start=content.find('href="/')
        index_end=content.rfind('<value')
        prefix="http://apps.webofknowledge.com/"
        link=prefix+content[index_start+7:index_end-3]
        link_list.append(link.replace("amp;",""))

    pattern = re.compile(ur'<value lang_id="">(.+?)</value>',re.S)
    s=pattern.finditer(html)
    title_list=[]
    for item in s:
        content=item.group()
        star=content.find('>')
        end=content.find('</value>')
        content = content[star+1:end].replace('<span class="hitHilite">','')
        content = content.replace('</span>','')
        title_list.append(content)

    print len(title_list),len(link_list)
    return title_list,link_list

def get_title_link(url):
    req=urllib2.Request(url,headers=headers)
    response=urllib2.urlopen(req)
    html=response.read()
    pattern =re.compile(ur'<span class="smallV110"></span><a class="smallV110 snowplow-full-record"(.+?)\n<value lang_id="">')
    s=pattern.finditer(html)
    link_list=[]
    for item in s:
        content=item.group()
        index_start=content.find('href="/')
        index_end=content.rfind('<value')
        prefix="http://apps.webofknowledge.com/"
        link=prefix+content[index_start+7:index_end-3]
        link_list.append(link.replace("amp;",""))

    return link_list

def parse_article_title(article_url):
    # req=urllib2.Request(article_url,headers=headers)
    # response=urllib2.urlopen(req)
    # html=response.read()
    global html
    pattern =re.compile(ur'class="title"(.+?)</value>',re.S)
    s=pattern.finditer(html)
    for item in s:
        content=item.group()
        content=content[content.find('<value>')+7:content.rfind('</value>')]
        content=content.replace('<span class="hitHilite">',"")
        content=content.replace("</span>","")
        content=content.lstrip().replace('\r','')
        content=content.replace('\n','')
        return content

def parse_article_abstract(article_url):
    # req=urllib2.Request(article_url,headers=headers)
    # response=urllib2.urlopen(req)
    # html=response.read()
    global html
    pattern= re.compile(ur'<div class="title3">Abstract</div>((?:.|\n)+?)<div class="title3">Keywords</div>')

    s=pattern.finditer(html)
    for item in s:
        content=item.group()

        # content=content[content.find('>')+1:content.find('</p>')]
        # content=content.replace('<span class="hitHilite">',"")
        # content=content.replace("</span>","")
        # content=content.replace('<p class="FR_field">',"")
        # content=content.replace('Abstract</div>','')
        # content=content.replace('<br>','')
        # content=content.lstrip().replace('\r','')
        # content=content.replace('\n','')

        content=content[content.find('"FR_field">')+11:content.find('</p>')]
        content=content.replace('<span class="hitHilite">',"")
        content=content.replace("</span>","")
        content=content.lstrip().replace('\r','')
        content=content.replace('\n','')
        content=content.replace('<br>','')
        return content

def parse_article_journal(article_url):
    # req=urllib2.Request(article_url,headers=headers)
    # response=urllib2.urlopen(req)
    # html=response.read()
    # pattern=re.compile(ur'<span class="sourceTitle">(.+?)</span>',re.S)

    global html
    pattern=re.compile(ur'class="sourceTitle">(.+?)</value>',re.S)


    s=pattern.finditer(html)
    for item in s:
        content=item.group()
        journal=content[content.find('<value>')+7:content.rfind('</value>')]
        return journal

def parse_article_year(article_url):
    # req=urllib2.Request(article_url,headers=headers)
    # response=urllib2.urlopen(req)
    # html=response.read()

    global html
    pattern =re.compile(ur'<span class="FR_label">Published:</span>(.+?)</p>',re.S)
    s=pattern.finditer(html)
    for item in s:
        content=item.group()
        year=content[content.find('<value>')+7:content.rfind('</value>')]
        return year

def get_meta_article(url):
    link_list=get_title_link(url)

    article_meta_list=[]
    for article_url in link_list:
        article_meta={}
        init(article_url)
        article_meta["title"]=parse_article_title(article_url)
        article_meta["year"]=parse_article_year(article_url)
        article_meta["journal"]=parse_article_journal(article_url)
        article_meta["abstract"]=parse_article_abstract(article_url)
        article_meta_list.append(article_meta)

    return article_meta_list
