import re
import os
import urllib2
import page_parser as parse

def read_keywords():
    f=open('key_word_urls')
    map_keywords={}
    for line in f.readlines():
        temp=line.split(' ')
        map_keywords[temp[0]]=temp[1]

    f.close()

    return map_keywords

def get_total_page(url):
    response=urllib2.urlopen(url)
    page_total=response.read()
    pattern=re.compile(ur'<span id="pageCount.bottom">(.+?)</span>',re.S)
    s=pattern.finditer(page_total)
    total_page_number=0
    for i in s:
        total_page_number=i.group()

    star=total_page_number.find('>')
    end=total_page_number.find('/')

    return int(total_page_number[star+1:end-1])


def get_all_data():
    map_word=read_keywords()
    list_word=[]
    file_name_list=[]
    for key in map_word.keys():
        file_name_list.append(key)
        list_word.append(map_word[key])

    title_set=set()

    for i in range(0,len(list_word)):
        print i,'/',len(list_word)
        url=list_word[i]
        total_page_number=get_total_page(url)

        if total_page_number==1:
            print i,'/',len(list_word),':',1,'/',total_page_number
            # parse.get_meta_article(url)
            articles=parse.get_meta_article(url)
            for j in range(0,len(articles)):
                articles_unit=articles[j]
                print "Title:",articles_unit["title"]
                if articles_unit["title"] not in title_set:
                    title_set.add(articles_unit["title"])
                    file_name=file_name_list[i]
                    write_to_file(articles_unit,file_name)
        else:
            for page in range(1,total_page_number+1):
                # print url
                print i,'/',len(list_word),':',page,'/',total_page_number

                end_page=url.find("&page=")
                url=url[0:end_page+6]+str(page)
                articles=parse.get_meta_article(url)
                for j in range(0,len(articles)):
                    articles_unit=articles[j]
                    print "Title:",articles_unit["title"]
                    if articles_unit["title"] not in title_set:
                        print i,'/',len(list_word),':',page,'/',total_page_number,':',j,'/',len(articles),articles_unit["title"]
                        title_set.add(articles_unit["title"])
                        file_name=file_name_list[i]
                        write_to_file(articles_unit,file_name)

    print 'Completed!'


def write_to_file(article_meta,file_name):
    file=open(os.path.join('./doc',file_name),'a+')
    print "Write to disk:"
    flag=True
    if article_meta["title"] is None:
        print "Title is None!"
        flag=False
        article_meta["title"]="None"
    if article_meta["year"] is None:
        print "Year is None!"
        flag=False
        article_meta["year"]="None"
    if article_meta["journal"] is None:
        print "journal is None!"
        flag=False
        article_meta["journal"]="None"
    if article_meta["abstract"] is None:
        print "abstract is None!"
        flag=False
        article_meta["abstract"]="None"

    file.write(article_meta["title"]+"^"+article_meta["year"]+"^"+article_meta["journal"]+"^"+article_meta["abstract"]+"\n")

    file.close()


def main():
    get_all_data()

if __name__ == '__main__':
    main()
