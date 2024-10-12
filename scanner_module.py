import requests
import re
import smtplib
import os
from bs4 import BeautifulSoup
from meal import Meal
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# URL of the webpage you want to scrape
url = 'https://dining.umich.edu/menus-locations/dining-halls/'
# urls = ['https://dining.umich.edu/menus-locations/dining-halls/' + s for s in ["Bursley", "East Quad", "Markley", "Mosher-Jordan", "North Quad", "South Quad", "Twigs at Oxford"]]
urls = ['https://dining.umich.edu/menus-locations/dining-halls/' + s for s in ["Bursley"]]
class Scanner:
    def __init__(self):
        self.calendar = list()
    def get_dining_hall(self, url):
        return url.split('/')[-1]
    def search_meal_time(self, courses_div, preceding_h3, time, dining_hall):
        if preceding_h3 and time in preceding_h3.get_text():
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
                                        name = ""
                                        this_allergen = ""
                                        calorie = ""
                                        protein = ""
                                        fat = ""
                                        carbs = ""
                                        dining_hall = dining_hall
                                        time = time
                                        for item_name in item_names:
                                            name = item_name.get_text()
                                            # print(name)
                                        for allergen in allergens:
                                            this_allergen = allergen.get_text()
                                            this_allergen = this_allergen.split('\n')
                                            #filter out empty strings and 'contains:'
                                            this_allergen = [x for x in this_allergen if x != '' and 'Contains:' not in x]
                                            # print(this_allergen)
                                        for calorie in calories:
                                            calorie = calorie.get_text()
                                            calorie = re.findall(r'\d+', calorie)[0]
                                            # print(calorie)
                                        for nutrition in nutrition_list:
                                            all_td = nutrition.find_all('td')
                                            nutrition_info = nutrition.find_all('tr', 'has-subitems')
                                            for td in all_td:
                                                if 'Protein' in td.get_text():
                                                    protein = td.get_text()
                                                    protein = re.findall(r'\d+', protein)[0]
                                                    # print(protein)

                                            # print(nutrition_info)
                                            if (len(nutrition_info) > 1):
                                                fat = nutrition_info[0].get_text()
                                                carbs = nutrition_info[1].get_text()
                                                fat = re.findall(r'\d+', fat)[0]
                                                carbs = re.findall(r'\d+', carbs)[0]
                                            
                                            # print(fat)
                                            # print(carbs)
                                            # print(text) #this is the time
                                        if name != "":
                                            this_meal = Meal(name, calorie, protein, carbs, fat, time, this_allergen, dining_hall)
                                            self.calendar.append(this_meal)
                                            # this_meal.display()

                else: 
                    print("no li_items")
        # else: 
        #     print(f"no {text} found")
    def scan(self, dining_halls, times):
        dining_halls = dining_halls[0]
        if (dining_halls == "Twigs"):
            url = 'https://dining.umich.edu/menus-locations/dining-halls/' + dining_halls + '-at-oxford/'
        elif (dining_halls == "Mojo"):
            url = 'https://dining.umich.edu/menus-locations/dining-halls/mosher-jordan/'
        else:    
            url = 'https://dining.umich.edu/menus-locations/dining-halls/' + dining_halls
        try:
            print("Start")
            print(url)
            # Send a GET request to the URL
            response = requests.get(url, verify=False)
            print("Good response")
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                print("Status code 200")
                dining_hall = self.get_dining_hall(url)
                # Get the HTML content
                html_content = response.text
                soup = BeautifulSoup(html_content, 'html.parser')
                # Find all divs with class="courses"
                courses_divs = soup.find_all('div', class_='courses')
                # Iterate through each courses div
                for courses_div in courses_divs:
                    # Find the preceding h3 tag
                    preceding_h3 = courses_div.find_previous_sibling('h3')
                    # Check if the preceding_h3 contains a food time
                    for time in times:
                        capitalized_time = time.capitalize()
                        self.search_meal_time(courses_div, preceding_h3, capitalized_time, dining_hall)
                # for meal in calendar:
                    # meal.display()
            else:
                print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error fetching the webpage: {e}")


#for some reason, li_items has ALL the items in the station, then each item individually which is why it prints twice