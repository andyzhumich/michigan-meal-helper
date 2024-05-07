import requests
import smtplib
import os
from bs4 import BeautifulSoup
from meal import Meal
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# URL of the webpage you want to scrape
url = 'https://dining.umich.edu/menus-locations/dining-halls/'
# urls = ['https://dining.umich.edu/menus-locations/dining-halls/' + s for s in ["Bursley", "East Quad", "Markley", "Mosher-Jordan", "North Quad", "South Quad", "Twigs at Oxford"]]
urls = ['https://dining.umich.edu/menus-locations/dining-halls/' + s for s in ["South Quad"]]

calendar = list()
for url in urls:
    try:
        print("Start")
        # Send a GET request to the URL
        response = requests.get(url, verify=False)
        print("Good response")
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Status code 200")
            print(url)
            # Get the HTML content
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            # Find all divs with class="courses"
            courses_divs = soup.find_all('div', class_='courses')
            # Iterate through each courses div
            for courses_div in courses_divs:
                # Find the preceding h3 tag
                preceding_h3 = courses_div.find_previous_sibling('h3')
                # Check if the preceding_h3 contains "Breakfast"
                if preceding_h3 and 'Dinner' in preceding_h3.get_text():
                    # Find all ul tags with class="courses_wrapper" within courses_div
                    courses_wrapper_uls = courses_div.find_all('ul', class_='courses_wrapper')
                    for courses_wrapper_ul in courses_wrapper_uls:
                        li_items = courses_wrapper_ul.find_all('li')
                        if li_items:
                            for li in li_items:
                                items = li.find_all('ul', class_='items')
                                if items:
                                    for item in items:
                                        item_names = item.find_all('div', class_='item-name')
                                        for item_name in item_names:
                                           print(item_name.get_text())
                                        allergens = item.find_all('div', class_='allergens')
                                        for allergen in allergens:
                                            print("ALLERGENS")
                                            print(allergen.get_text())
                        else: 
                            print("no li_items")
        else:
            print(f"Failed to fetch the webpage. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")


#for some reason, li_items has ALL the items in the station, then each item individually which is why it prints twice