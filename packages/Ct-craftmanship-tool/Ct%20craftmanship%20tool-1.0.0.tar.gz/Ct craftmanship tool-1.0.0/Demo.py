import xlsxwriter
import pandas as pd
import chardet
import requests
from urllib.parse import urlencode
from requests.auth import HTTPBasicAuth
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import *
import time
import re

global temp
#Destination and source file path
destination='D:/MyFolder/demo.xlsx'
source='D://MyFolder//Source.csv'

workbook = xlsxwriter.Workbook(destination)
worksheet = workbook.add_worksheet("my sheet")

#Determining the type of encoding and it resulted in UTF-16
with open(source, 'rb') as rawdata:
    result = chardet.detect(rawdata.read(10000000000))

#Reading source csv file with "\t" delimeter and took row 6 as header   
df = pd.read_csv(source,encoding='UTF-16', sep="\t",header=6)





#Renaming columns







#1 day=24 hours
#1 hour=0.14 days
df.insert(0,"RollNo", "")

for ind in df.index:
    duration=df["Duration"].str[:3]
  
    temp = re.findall(r'\d+', duration.to_string())
    
df["Duration"]=duration


driver = webdriver.Chrome("D:/MyFolder/chromedriver.exe")  #Path to chromeDriver 
driver.set_window_position(-10000,0)
driver.get("https://scd.siemens.com/")

 #Clicking on cancel in login pop up so that we can login using smart card
conent=driver.find_element_by_xpath("//div[@class='modal-footer']/div[@class='arrow-link btn-cancel']").click()

smartcard_login = '//*[@id="loginSmartCard"]/div[2]'
pop_up=driver.find_element_by_xpath(smartcard_login).click()


for index, row in df.iterrows():
    search_string=row['Full Name'].split('(')[0] 
    #Using Selenium
    if(any(map(str.isdigit, search_string))):
        continue
   
    matched_elements = driver.get("https://scd.siemens.com/luz/IdentitySearch?cn=" +
                                     search_string +" &maxanz=50&suchart=schnell&tab=tabs-1")

    try:
        driver.find_element_by_xpath('//*[@id="searchresults"]/table')
        driver.find_element_by_xpath('/html/body/div[1]/div[9]/div/div/div[2]/div[5]/table/tbody/tr[2]/td[1]/a').click()
    
    except NoSuchElementException:
        pass
    
    GID=driver.find_element_by_xpath('//*[@id="main"]/div[3]/div[1]/table/tbody/tr[10]/td[2]/span/a')
    
    
   
    df.at[index,'RollNo']=GID
time.sleep(100)
driver.close()


df = df.rename(columns={'Join Time': 'FromDate', 'Leave Time': 'ToDate','Full Name':'TrainerName'})

#Inserting some new columns 

df["FromDate"]=df['FromDate'].str[:8]
df["ToDate"]=df["ToDate"].str[:8]

df.insert(0,"RollNo", "")
df.insert(1, 'Location', 'Banglore')



df.insert(5,"Vendor","NA")
df.insert(7,'CourseCategory',"NA")
df.insert(8,'CourseTopic',df.iloc[2].str[:8])
df.insert(9,"InternalOrExternal","Internal")
df.insert(10,"TrainingSource", "NA")


df.reindex(columns=["RollNo","Location","FromDate","ToDate","Duration","Vendor","TrainerName","CourseCategory", "CourseTopic","InternalOrExternal","TrainingSource"])


df.drop("Email", inplace=True,axis=1)
df.drop("Role",inplace=True,axis=1)

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter("D:/MyFolder/demo.xlsx",engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1')

# Close the Pandas Excel writer and output the Excel file.
writer.save()