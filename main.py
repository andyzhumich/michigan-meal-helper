from planner import Planner, UserPreferences
from local_scanner import Scanner
from flask import Flask
app = Flask(__name__) 

def main():
    user_pref = UserPreferences(2000, 100, 200, 50, [], True, False, True, True, ['Twigs'])
    scanner = Scanner()
    scanner.scan()
    #list every unique allergen in the calendar
    allergens = set()
    for meal in scanner.calendar:
        allergens.update(meal.allergens)
    print(allergens)
    # planner = Planner(scanner.calendar, user_pref)
    # planner.filter()
    # planner.make_meal_plan(500)
    # planner.display()


if __name__ == "__main__":
    main()

