import requests
from bs4 import BeautifulSoup as bs4
from urllib.request import urlopen
from datetime import datetime
import pymongo

try:

    url = "https://internshala.com/internships/work-from-home-jobs"

    uClient = urlopen(url)
    internshala_page = uClient.read()
    uClient.close()

    page_beautify = bs4(internshala_page, "html.parser")

    total_no_pages = page_beautify.find("span", {"id":"total_pages"}).text

    profiles = []

    for i in range(1, int(total_no_pages)+1):
        next = url+"/page-"+str(i)

        next_page_content = requests.get(next)
        beautify_nextPage = bs4(next_page_content.text, "html.parser")
        big_boxes = beautify_nextPage.find_all("div", {"class":"individual_internship"})

        for box in big_boxes:
            try:
                now = datetime.now()
                date_time = now.strftime("%Y-%m-%d %H:%M:%S")
            except :
                date_time = "2/11/2020"

            try:
                profile = box.find("div", {"class":"profile"}).a.text
            except:
                profile = "Nothing"

            try:
                company = box.find("div", {"class":"company_name"}).a.text.strip().replace("\n", "")
            except :
                company = "Nothing"
            
            try:
                location = box.find("a", {"class":"location_link"}).text
            except:
                location = "Nothing"

            try:
                start_date = box.find("span", {"class":"start_immediately_desktop"}).text
            except:
                start_date = "Nothing"

            try:
                stipend = box.find("span", {"class":"stipend"}).text
            except:
                stipend = "Nothing"

            try:
                duration_row = box.find_all("div", {"class":"other_detail_item"})
                duration = duration_row[1].find("div", {"class":"item_body"}).text.strip().replace("\n", "")
            except:
                duration = "Nothing"

            try:
                apply_by = box.find("div", {"class":"apply_by"})
                apply_by_date = apply_by.find("div", {"class":"item_body"}).text
            except:
                apply_by_date = "Nothing"

            try:
                offer = box.find("div", {"class":"label_container label_container_mobile"}).text.strip().replace("\n", "")
            except :
                offer = "Nothing"


            detail_link = [a['href'] for a in box.find_all("a", {"class":"view_detail_button"}, href=True)]
            detail_page = requests.get("https://internshala.com/"+str(detail_link[0]))
            beautify_detail_page = bs4(detail_page.text, "html.parser")

            try:
                skills_list = []
                skills_set = beautify_detail_page.find_all("span", {"class":"round_tabs"})
                for i in skills_set:
                    skills_list.append(i.text)
            except :
                skills_list = []


            myDict = {
                "Date Time":date_time,
                "profile":profile, 
                "company":company,
                "Location":location,
                "Start Date":start_date,
                "Stipend":stipend,
                'Duration':duration,
                'Apply by Date':apply_by_date,
                "Offer":offer,
                "Skills and Perks":skills_list,
            }

            profiles.append(myDict)

    print(profiles)
except Exception as e:
    print(e)



