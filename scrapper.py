from requests import request
from selenium import webdriver
from bs4 import BeautifulSoup 
import time 
import csv
import requests
from selenium.webdriver.common.by import By 

start_url="https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser=webdriver.Chrome("chromedriver.exe")
browser.get(start_url)
time.sleep(10)
headers=["name","light_years_from_earth","planet_mass","stellar_magnitude","discovery_date""hyperlink", "planet_type", "planet_radius", "orbital_radius", "orbital_period", "eccentricity"]

planetdata=[]


def scrap():
    for i in range(1,5):
        while True:
            time.sleep(2)
            soup=BeautifulSoup(browser.page_source,"html.parser")
            currentPage=int(soup.find_all("input",attrs={"class","page_num"})[0].get("value"))
            if currentPage<i:
                browser.find_element(By.XPATH,value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif currentPage>i:
                browser.find_element(By.XPATH,value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            else:
                break

        for ultag in soup.find_all("ul",attrs={"class","exoplanet"}):
            litags=ultag.find_all("li")
            templist=[]
            for index ,litag in enumerate(litags):
                if index==0:
                    templist.append(litag.find_all("a")[0].contents[0])
                else:
                    try:
                        templist.append(litag.contents[0])
                    except:
                        templist.append("")
            hyperlinkTag=litags[0]
            templist.append("https://exoplanets.nasa.gov"+hyperlinkTag.find_all("a",href=True)[0]["href"])
            planetdata.append(templist)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
    
scrap()
newplanetsdata=[]
def scrapdata(x):
    try:
        page=requests.get(x)
        soup=BeautifulSoup(page.content,"html.parser")
        templist=[]
        for trtag in soup.find_all("tr",attrs={"class":"fact_row"}):
            tdtags=trtag.find_all("td")
            for tdtag in tdtags:
                try:
                    templist.append(tdtag.find_all("div",attrs={"class":"value"})[0].contents[0])
                except:
                    templist.append("")
        newplanetsdata.append(templist)
    except:
        time.sleep(1)
        scrapdata(x)

for index,data in enumerate(planetdata):
    scrapdata(data[5])
    print(f"Scrapping At Hyperlink {index+1} is completed")
finalplanetdata=[]
for index,data in enumerate(planetdata):
    newdata=newplanetsdata[index]
    newdata=[elem.replace("\n","") for elem in newdata]           
    newdata=newdata[:7]
    finalplanetdata.append(data+newdata)

with open("final.csv","w") as f :
        csvWritter=csv.writer(f)
        csvWritter.writerow(headers)
        csvWritter.writerows(finalplanetdata)
                