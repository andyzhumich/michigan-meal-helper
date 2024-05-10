#This file will take the information from calendar and plan the meal plan for the day
#The meal plan will be planned based on the user's preferences


#defines the planner class, which consists of a list of meals
#planner class definition
class UserPreferences:
    def __init__(self, calories, protein, carbs, fat, allergens, breakfast, brunch, lunch, dinner, dining_halls):
        self.calories = calories #desired calories (int)
        self.protein = protein
        self.carbs = carbs
        self.fat = fat
        self.allergens = allergens #list of allergens
        self.breakfast = breakfast #bool for each of these
        self.brunch = brunch
        self.lunch = lunch
        self.dinner = dinner
        self.dining_halls = dining_halls #list of acceptable dining halls


        
class Planner:
    def __init__(self, calendar, user_preferences):
        self.calendar = calendar
        self.user_preferences = user_preferences
        self.meal_plan = list()
    def filter(self):
        bad_food_items = list()
        #for each meal in the calendar, check if it fits the user's preferences (dining hall, allergens, time)
        for meal in self.calendar:
            allergen_bool = False
            #check if the meal is in a dining hall the user likes
            if meal.dining_hall not in self.user_preferences.dining_halls:
                bad_food_items.append(meal)
                continue
            #check if the meal has any allergens the user dislikes
            for allergen in meal.allergens:
                if allergen in self.user_preferences.allergens:
                    bad_food_items.append(meal)
                    allergen_bool = True
                    break
            if allergen_bool:
                continue

            #check if the meal is at a time the user wants to eat
            if meal.time == 'Breakfast' and not self.user_preferences.breakfast:
                bad_food_items.append(meal)
                continue
            if meal.time == 'Brunch' and not self.user_preferences.brunch:
                bad_food_items.append(meal)
                continue
            if meal.time == 'Lunch' and not self.user_preferences.lunch:
                bad_food_items.append(meal)
                continue
            if meal.time == 'Dinner' and not self.user_preferences.dinner:
                bad_food_items.append(meal)
                continue
            #if the meal fits the user's preferences, add it to the meal plan
        self.meal_plan = [meal for meal in self.calendar if meal not in bad_food_items]
    def make_meal_plan(self):
        #make a meal plan based on the user's preferences
        #this will be done by adding meals to the meal plan until the desired calories are met
        #the meals will be added in order of time (breakfast, brunch, lunch, dinner)
        #if there are not enough meals to meet the desired calories, the user will be notified
        #if there are too many meals to meet the desired calories, the user will be notified
        #if the desired calories are met, the user will be notified
        pass
    def display(self):
        for meal in self.meal_plan:
            meal.display()