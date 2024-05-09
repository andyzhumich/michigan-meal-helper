#This file will take the information from calendar and plan the meal plan for the day
#The meal plan will be planned based on the user's preferences


#defines the planner class, which consists of a list of meals
#planner class definition
class UserPreferences:
    def __init__(self, calories, protein, carbs, fat, allergens, breakfast, brunch, lunch, dinner):
        self.calories = calories
        self.protein = protein
        self.carbs = carbs
        self.fat = fat
        self.allergens = allergens
        self.breakfast = breakfast
        self.brunch = brunch
        self.lunch = lunch
        self.dinner = dinner


        
class Planner:
    def __init__(self, calendar, user_preferences):
        self.calendar = calendar
        self.user_preferences = user_preferences
        self.meal_plan = list()
    def plan(self):
        #for each meal in the calendar, check if it fits the user's preferences
        for meal in self.calendar:
            #if the meal fits the user's preferences, add it to the meal plan
            self.meal_plan.append(meal)
    def display(self):
        for meal in self.meal_plan:
            meal.display()