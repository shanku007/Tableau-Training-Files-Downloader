from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import os

class TableauDownloader:
    
    
    def __init__(self,link="https://www.tableau.com/learn/training"):
        self.url = link
        self.Video = True
        self.Transcript = True
        self.Other = True
        
        
        
    def get_page_content_without_java_script_execution(self,url):
        """To get the content of the page 
        
        without executing the javascript code on the website"""
        
        page_content = requests.get(url)
        return page_content
    
    
    
    def get_page_content__with_java_script_execution(self,link):
        """To get the content of the page 
        
        after executing the javascript code on the website"""
        driver = webdriver.Firefox()
        driver.get(link)
        sauce = driver.page_source
        driver.quit()
        return sauce
        
    
    
    
    def prepare_soup(self,page_content,parser="html5lib",extract_content=True):
        if(extract_content):
            return BeautifulSoup(page_content.content,parser)
        else:
            return BeautifulSoup(page_content,parser)
    
    
    
    
    def get_links_category_wise(self):
        page_content = self.get_page_content_without_java_script_execution(self.url) #Getting the content of the page 
        soup = self.prepare_soup(page_content) 
        links  = soup.find_all('a',class_='video-playlist__link')
        video_links = {}
        for link in links:
            video_cat = link['href'].split('&')[2].split('=')[1]
            if video_cat not in video_links:
                video_links[video_cat] = []
            video_links[video_cat].append(link['href'])
        return video_links
    
    
    
    def save_file(self,files_url,files_name):
        for i in range(len(files_name)):
            print(files_url[i])
            r = requests.get(files_url[i], stream = True) 
            with open(files_name[i],"wb") as file: 
                for chunk in r.iter_content(chunk_size=1000000): 
                # writing one chunk at a time to pdf file 
                    if chunk: 
                        file.write(chunk)
              
            
                
    def get_links_of_downloadable_item(self,soup):
        downloadable_items_links = {}
        video_link = soup.find_all('a',class_='mp4-download-link link link--download')[0]['href']
        downloadable_items_links['name'] = soup.find_all('h4')[0].string
        downloadable_items_links['video'] = video_link
        other_links = soup.find_all('div',class_='gallery-grid__item')
        for i in range(len(other_links)):
            key = other_links[i].h5.string
            value = other_links[i].a['href']
            downloadable_items_links[key] = value
            
        return downloadable_items_links
            
        
    def file_names(self,filename_prefix,key,value,is_Video):
        if(is_Video):
            return str(filename_prefix)+str(key)+'.mp4'
        else:
            ext = value.split('.')[-1]
            return str(filename_prefix)+str(key)+'.'+str(ext)
        
        
    def download_files(self,location,category,category_index):
        links = self.get_links_category_wise()
        index = 0
        for vidcat in category:
            i = category_index[index]
            folder = str(location)+'/'+str(i)+str(vidcat)
            if(not os.path.isdir(folder)):
                os.mkdir(str(location)+'/'+str(i)+str(vidcat))
            videos_to_download_this_category = links[vidcat]
            j = 1
            for each_video_link in videos_to_download_this_category:
                if(self.Video):
                    sauce  = self.get_page_content__with_java_script_execution(each_video_link) #To get the page content after executing javascript in the page
                    soup = self.prepare_soup(sauce,'lxml',False)
                else:
                    content_of_page = self.get_page_content_without_java_script_execution(each_video_link)
                    soup = self.prepare_soup(content_of_page,'lxml',True)
                    
                    
                downloadable_items_links = self.get_links_of_downloadable_item(soup) 
                
                
                video_name = downloadable_items_links['name']
                folder_name = str(location)+'/'+str(i)+str(vidcat)+'/'+str(j)+str(video_name)
                if(not os.path.isdir(folder_name)):
                    os.mkdir(str(location)+'/'+str(i)+str(vidcat)+'/'+str(j)+str(video_name))
                file_prefix = str(location)+'/'+str(i)+str(vidcat)+'/'+str(j)+str(video_name)+'/'
                files_to_download_name = []
                files_to_download_links = []
                if(self.Video and self.Transcript and self.Other):   #To Download Everythin
                    for key,value in downloadable_items_links.items():
                        if(key=='name'):
                            continue
                        elif(key!='video'):
                            filename = self.file_names(file_prefix,key,value,False)
                            files_to_download_links.append(value)
                            files_to_download_name.append(filename)
                        else:
                            filename = self.file_names(file_prefix,key,value,True)
                            files_to_download_links.append(value)
                            files_to_download_name.append(filename)
                            
                
                
                elif(self.Video and self.Other and not self.Transcript): #To Download Video and Data,Workbook etc other than Transcript
                    for key,value in downloadable_items_links.items():
                        if(key=='Transcript' or key=='name'):
                            continue
                        elif(key!='video'):
                            filename = self.file_names(file_prefix,key,value,False)
                            files_to_download_links.append(value)
                            files_to_download_name.append(filename)
                        else:
                            filename = self.file_names(file_prefix,key,value,True)
                            files_to_download_links.append(value)
                            files_to_download_name.append(filename)
                            
                            
                elif(self.Other and not self.Video and not self.Transcript): #Data,Workbook etc other than Transcript
                    for key,value in downloadable_items_links.items():
                        if((key=='Transcript') or (key == 'video') or (key=='name')):
                            continue
                        else:
                            filename = self.file_names(file_prefix,key,value,False)
                            files_to_download_links.append(value)
                            files_to_download_name.append(filename)
                
                elif(self.Video and not self.Other and not self.Transcript): #To Download Video and Data,Workbook etc other than Transcript
                    for key,value in downloadable_items_links.items():
                        if(key=='video'):
                            filename = self.file_names(file_prefix,key,value,True)
                            files_to_download_links.append(value)
                            files_to_download_name.append(filename)
                        else:
                            continue
                
                
                print("Downloading "+str(video_name) + "........")
                self.save_file(files_to_download_links,files_to_download_name)
                
                
                
                
                
                
                j += 1
            
            index += 1
            
    def download_data(self):
        print("Welcome To Tableau Files Downloader.")
        print("Devloped by Shankar Jha")
        print("""Following are the topics of Video""")
        categories = list(self.get_links_category_wise().keys())
        i = 1
        for category in categories:
            print(i,category)
            i += 1
        print("""Enter the number corresponding to each category which files you want to Download
        Seperate your choice with space""")
        category_index = list(map(int,input().split()))
        categories_to_download = []
        for index in category_index:
            categories_to_download.append(categories[index-1])
        print("Enter the Location")
        location = input()

        while(not os.path.isdir(location)):
            print(location + " doesnot exist")
            print('-'*10)
            print("Enter a valid location")
            location = input()
        
        print("""Enter Your Choice
        1. To Download Videos and Exercise Workbook, Data Sets etc only
        2. To Download Videos Only
        3. To Download Exercise Workbook, Data Sets etc only
        
        Press any other key to Download all""")
        
        choice = int(input())
        if(choice==1):
            self.Transcript = False
        elif(choice==2):
            self.Transcript = False
            self.Other = False
        elif(choice==3):
            self.Video = False
            self.Transcript = False
        
        print("Starting to Download Your Choices")
        self.download_files(location,categories_to_download,category_index)
        
        return "Sucessfully Downloaded your choices"
            
    
if __name__ == "__main__":
    url = "https://www.tableau.com/learn/training"
    video_downloader = TableauDownloader(url)
    video_downloader.download_data()

    
