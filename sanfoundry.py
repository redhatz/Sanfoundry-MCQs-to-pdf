from bs4 import BeautifulSoup as bs
from sanUrls import UrlsClass
from tqdm import tqdm
import requests
import re
import os
import pdfkit

class Sanfoundry(object):
    
    def __init__(self):
        self.mode = int(input("\nEnter 0 for Manual Mode and 1 for Auto Mode: "))
        self.extract_line = r"<p>\s*<strong>.*</strong>.*</p>"
        self.classes = lambda x: x and x.startswith(('mobile-content', 'desktop-content', 'sf-nav-bottom', 'sf-mobile-ads'))
        
        if self.mode == 1:
            self.auto()
            
        else:
            self.url = input("\nEnter Sanfoundry MCQ URL: ")
            self.scrape()
    
    def auto(self):
        urlList = UrlsClass().getUrls()
        print("\n")
        for i in tqdm(range(0, len(urlList)), desc ="Saving Mcqs"):
            self.url = urlList[i]
            self.scrape()
        self.savepdf()
        
    def scrape(self):
        with requests.Session() as s:
            r = s.get(self.url)
            soup = bs(r.content, "html5lib")
            div = soup.find("div", {"class":"entry-content"})
            div.attrs = {}
            [tag.extract() for tag in div(['script','a'])]
            [tag.extract() for tag in div.find_all(["div"], {"class":self.classes})]
            [tag.extract() for tag in div.find_all("span", {"class":"collapseomatic"})]
            [tag.extract() for tag in div.find_all("div") if tag.text == "advertisment"]
            for tags in div.find_all(True): tags.attrs = {}
            data = ' '.join(str(div).split())
            data = re.sub(self.extract_line, "", data)

            filename = self.url.split("/")[3]
            self.check_dir()
            with open(f"Output/{filename}.html", "w+", encoding="utf-8") as file:
                file.write(str(bs(data, "html5lib").prettify()))
                file.close()
                
            

            if self.mode == 0:
                more = input("Scrape More? (Y/N): ").lower().strip()
                try:
                    if more[0] == 'y':
                        self.url = input("\nEnter Sanfoundry MCQ URL: ")
                        self.scrape()
                    elif more[0] == 'n':
                        exit()
                    else:
                        print('Invalid Input')
                except Exception as error:
                    print("An Error Occured: ")
                    print(error)
                    
        
                    
    def check_dir(self):
        if not os.path.exists('Output'):
            os.makedirs('Output')
    
    
    def savepdf(self):
        cd=os.getcwd()
        cd1=os.path.join(cd,"Output")
        os.chdir(cd1)
        files_arr=os.listdir()
        out_f = input('Enter The ouput pdf name: ')
        extension=".pdf"
        out=out_f+extension
        pdfkit.from_file(files_arr, out)
        for file in files_arr:
           if file.endswith('.html'):
              os.remove(file)
        
        
    
    
Sanfoundry()