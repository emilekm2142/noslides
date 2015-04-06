import urllib.request
from bs4 import BeautifulSoup
from django.views.decorators.csrf import csrf_exempt
import kwejk.requests as requests
@csrf_exempt
class ShortGallery():
    def __init__(self,url):
        self.kwejk="http://kwejk.pl"
        self.besty="http://besty.pl"
        self.imageslist=[]
        self.url=url
        self.title=''
        self.ua = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
        self.headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", 'User-Agent': self.ua}

    def run(self):
        self.soup=self.getURL()
        print (self.soup)
        self.downloadImages()
        self.view()
        return self.output
        
    def getURL(self,url=None):
        if url is None:
            u=requests.get(self.url,headers=self.headers)
            soup=BeautifulSoup(u.text)
        else:
            u=requests.get(url,headers=self.headers)
            soup=BeautifulSoup(u.text)
        return soup
    
    def downloadImages(self):
        if "kwejk" in self.url:
            self.title=self.soup.title.text
            gallery=self.soup.find('div',{'class':'jcarousel-wrapper'})
            images=gallery.find_all("a")
            for i in images:
                url=i['href']
                if url=="#":break
                soup=self.getURL(url)
                largepic=soup.find('div',{"class":"self"})
                image=largepic.img['src']
                self.imageslist.append(image)

        elif "besty" in self.url:
            self.title=self.soup.title.text
            gallery=self.soup.find('div',{'id':'gallery-wrapper'})
            images=gallery.find_all("a")
            for i in images:
                url=self.besty+i['href']
                x=urllib.request.urlopen(url)
                soup=BeautifulSoup(x)
                largepic=soup.find('div',{"id":"largepic"})
                image=largepic.img['src']
                self.imageslist.append(image)

        else:
            self.imageslist=['">NO NIESTETY ZŁY URL<br']
        print("koniec zbierania obrazkow")
    def view(self):
        head="""
        <!DOCTYPE html>
        <html lang="pl">
        <head>
        <meta charset="utf-8">
        <style>


        .image{
        display:block;
            margin:auto;
            }
        #container{
        width:960px;

        margin:auto;
        }

        img{
        border:5px solid rgba(200,200,200,0.6);
        }

        </style>
        <title>Krótka galeria z kwejka ^^</title>
        </head>
        """
        body="""
        <body>
        <section id="container">
        """
        end="""
        </section>
        </body>
        </html>
        """
        images=''
        for i in self.imageslist:
            images=images+'<img class="image" src="'+i+'"><br>'

        self.output=head+body+images+end