'''
Author: your name
Date: 2021-07-06 09:22:09
LastEditTime: 2021-07-22 21:03:05
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \get_ris\get_ris\get_ris.py
'''
#-*- encoding: UTF-8 -*-
import requests
import re
import os
import sys
import json

session = requests.Session()
session.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'}

class Article():
    def __init__(self,title,authors,year,type,publisher,abstract) -> None:
        self.title = title
        self.year = year
        self.type = type
        self.authors = authors
        self.publisher = publisher
        self.abstract = abstract

    def convert_to_Endnote(self):
        content = ''
        content+=f'%0 {self.type}\n'
        for author in self.authors:
            content+=f'%A {author}\n'
        content+=f'%T {self.title}\n'
        content+=f'%J {self.publisher}\n'
        content+=f'%D {self.year}\n'
        content+=f'%X {self.abstract}\n'
        return content
        
    def __repr__(self) -> str:
        return self.convert_to_Endnote()
class IEEEDownloader:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'}
    def get_download_url(self,session,ar_num):
        base_url = 'https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber='+str(ar_num)
        r = session.get(base_url,stream = True).content
        # 在接收到的html中获取pdf的下载位置
        url = re.findall('iframe src="(.*?)" frameborder.*?',str(r))[0]
        return url

    def download_url(self,url,path,out_file):
        r = requests.get(url,stream = True)
        with open(path+out_file,'wb') as f:
            f.write(r.content)
    '''
    @description: Download pdf according to ar_number info
    @param {*} self
    @param {*} arm_number
    @return {*}
    '''
    def download_pdf(self,ar_number):
        url = self.get_download_url(session=self.session,ar_num=ar_number)
        self.download_url(url=url,path = '.\\',out_file=f'{ar_number}.pdf')
        return os.getcwd()+'\\'+ar_number+'.pdf'

def get_download_url(ar_num):
    base_url = 'https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber='+str(ar_num)
    r = session.get(base_url,stream = True).content
    # 在接收到的html中获取pdf的下载位置
    url = re.findall('iframe src="(.*?)" frameborder.*?',str(r))[0]
    return url

def download_url(url,path,out_file):
    r = requests.get(url,stream = True)
    with open(path+out_file,'wb') as f:
        f.write(r.content)

def get_info_by_id(ar_number):
    url = f'https://ieeexploreapi.ieee.org/api/v1/search/articles?article_number={ar_number}&apikey=ab75bvpx4e7f6yp4setb6y24'
    content = session.get(url,stream = True,verify=False).content
    data = json.loads(content.decode())

    if(data['total_records'] is 0):
        print('No file')
        return
    elif(data['total_records']>1):
        print('File more than one, get the first one')
    article = data['articles'][0]

    _title = article['title']
    _authors_raw = article['authors']['authors']
    _authors = []
    for author in _authors_raw:
        _authors.append(author['full_name'])
    _abstract = article['abstract']
    _type = article['content_type']
    _publisher = article['publication_title']
    _year = article['publication_year']

    return Article(title=_title,authors=_authors,year=_year,type=_type,publisher=_publisher,abstract=_abstract)
@DeprecationWarning
def download_ris(id,path):
    '''
    retrieve ris for the file
    '''
    ris_url = 'https://ieeexplore.ieee.org/xpl/downloadCitations'
    data = {
        'recordIds': id,
        'download-format': 'download-ris',
        'citations-format': 'citation-only'
    }
    down_path = path+'\\'+id+'.ris'
    res = requests.post(ris_url,data=data)
    with open(down_path,'wb+') as f:
        f.write(res.content)
    print(f'RIS has been downloaded to {down_path}')
    os.system(down_path)

@DeprecationWarning
def save_path(path):
    with open('.\\download_path.txt','w') as f:
        f.write(path)

@DeprecationWarning
def read_path():
    if(os.path.exists('.\\download_path.txt')):
        with open('.\\download_path.txt','r') as f:
            return f.readlines()[0]
    else:
        path = input("Input download path:\n")
        save_path(path)
        return path
        
def start():
    url = sys.argv[1]
    id = re.findall("(\d{6,})",url)[0]
    print(f"RIS try to download")
    try:
        info = get_info_by_id(id)
        with open('.\\temp.ris','w') as f:
            f.write(str(info))
        print(f'RIS has been downloaded to temp.ris')
        os.system('.\\temp.ris')
        
    except Exception as e:
        print(e)
def start_pdf():
    down = IEEEDownloader()
    url = sys.argv[1]
    id = re.findall("(\d{6,})",url)[0]
    print(f"RIS try to download")
    try:
        file_path = down.download_pdf(id)
        print(f'file is {file_path}')
        info = get_info_by_id(id)
        with open('.\\temp.ris','w') as f:
            f.write(str(info))
            f.write(f'%> {file_path}')
        print(f'RIS has been downloaded to temp.ris')
        os.system('.\\temp.ris')
        
    except Exception as e:
        print(e)
        
if __name__ == '__main__':
    # print(sys.argv[1])
    start_pdf()
    
