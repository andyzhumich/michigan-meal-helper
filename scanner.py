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
urls = ['https://dining.umich.edu/menus-locations/dining-halls/' + s for s in ["Twigs at Oxford"]]

calendar = list()
def search_meal_time(courses_div, preceding_h3, text):
    if preceding_h3 and text in preceding_h3.get_text():
                    # Find all ul tags with class="courses_wrapper" within courses_div
        courses_wrapper_uls = courses_div.find_all('ul', class_='courses_wrapper')
        for courses_wrapper_ul in courses_wrapper_uls:
            li_items = courses_wrapper_ul.find_all('li')
            if li_items:
                for li in li_items:
                    items = li.find_all('ul', class_='items')
                    if items:
                        for item in items:
                            listed_items = item.find_all('li')
                            if listed_items:
                                for listed_item in listed_items:
                                    item_names = listed_item.find_all('div', class_='item-name')
                                    allergens = listed_item.find_all('div', class_='allergens')
                                    calories = listed_item.find_all('tr', class_='portion-calories thick-border')
                                    nutrition_list = listed_item.find_all('div', class_='nutrition-wrapper')
                                              
                                    for item_name in item_names:
                                        print(item_name.get_text())
                                        name = item_name.get_text()
                                    for allergen in allergens:
                                        allergens = allergen.get_text()
                                    for calorie in calories:
                                        print(calorie.get_text()[10::])
                                        calorie = calorie.get_text()[10::]
                                    for nutrition in nutrition_list:
                                        all_td = nutrition.find_all('td')
                                        nutrition_info = nutrition.find_all('tr', 'has-subitems')
                                        for td in all_td:
                                            if 'Protein' in td.get_text():
                                                protein = td.get_text()[9::]
                                                print("PROTEIN", td.get_text()[9::])
                                        fat = nutrition_info[0].get_text()[10::]
                                        carbs = nutrition_info[1].get_text()[21::]
                                        print("FAT", fat)
                                        print("CARBS", carbs)
                                    time = text
                                    print(time)
                                    
            else: 
                print("no li_items")
    else: 
        print(f"no {text} found")

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
                for text in ["Breakfast", "Brunch", "Lunch", "Dinner"]:
                    search_meal_time(courses_div, preceding_h3, text)
        else:
            print(f"Failed to fetch the webpage. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")


#for some reason, li_items has ALL the items in the station, then each item individually which is why it prints twice