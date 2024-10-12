#This file will take the information from calendar and plan the meal plan for the day
#The meal plan will be planned based on the user's preferences
import random

#defines the planner class, which consists of a list of meals
#planner class definition]


class UserPreferences:
    def __init__(self, calories, protein, carbs, fat, allergens, meal_times, dining_halls):
        self.calories = int(calories) #desired calories (int)
        self.protein = int(protein)
        self.carbs = int(carbs)
        self.fat = int(fat)
        self.allergens = allergens #list of allergens
        self.breakfast = False
        self.brunch = False
        self.lunch = False
        self.dinner = False
        for i in meal_times:
            if i == 'breakfast':
                self.breakfast = True
            if i == 'brunch':
                self.brunch = True
            if i == 'lunch':
                self.lunch = True
            if i == 'dinner':
                self.dinner = True

        self.number_of_meals = len(meal_times) #number of meals the user wants to eat
        self.dining_halls = dining_halls #list of acceptable dining halls


        
class Planner:
    def __init__(self, calendar, user_preferences):
        self.calendar = calendar
        self.user_preferences = user_preferences
        self.filtered_meals = list()
        self.random_meals = list()
        self.list_of_weighted_meal_plans = list()
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
        self.filtered_meals = [meal for meal in self.calendar if meal not in bad_food_items]

    def plan_individual_meal(self, time, num):
        #num is the number of possible meals it makes, uses weighted sum to rank them
        #make random meal plan for each meal
        #first round is random and focused on fitting calroies, lsat round is all the meals combined and focused on macros + caloreis
        goal_calories = self.user_preferences.calories / self.user_preferences.number_of_meals
        meals_in_this_time = [meal for meal in self.filtered_meals if meal.time == time]
        possible_meal_plan = list()
        for i in range(num):
            possible_meal_plan = list()
            current_calories = 0
            while current_calories < goal_calories * .9:
                random_meal = meals_in_this_time[random.randint(0, len(meals_in_this_time) - 1)]
                possible_meal_plan.append(random_meal)
                # print(random_meal.name)
                if (random_meal.calories != ''):
                    current_calories += int(random_meal.calories)
            self.random_meals.append(possible_meal_plan)


    def make_meal_plan(self, num):
        #make a meal plan based on the user's preferences
        #this will be done by adding meals to the meal plan until the desired calories are met
        #the meals will be added in order of time (breakfast, brunch, lunch, dinner)
        #if there are not enough meals to meet the desired calories, the user will be notified
        #if there are too many meals to meet the desired calories, the user will be notified
        #if the desired calories are met, the user will be notified
        if self.user_preferences.breakfast:
            self.plan_individual_meal('Breakfast', num)
        if self.user_preferences.brunch:
            self.plan_individual_meal('Brunch', num)
        if self.user_preferences.lunch:
            self.plan_individual_meal('Lunch', num)
        if self.user_preferences.dinner:
            self.plan_individual_meal('Dinner', num)
        list_of_random_meal_plans = list()
        for x in range(num): 
            random_meal_plan = list()
            for i in range(self.user_preferences.number_of_meals):
                index = random.randint((i)*num,(i+1)*num-1)
                random_meal_plan.append(self.random_meals[index])
            list_of_random_meal_plans.append(random_meal_plan)

        #calculate the difference in calories and macros for each meal plan
        desired_values = [self.user_preferences.calories, self.user_preferences.protein, self.user_preferences.carbs, self.user_preferences.fat]
        for r_m_p in list_of_random_meal_plans:
            weight_and_meal = list()
            weight_and_meal.append(calculate_weights(r_m_p, desired_values))
            weight_and_meal.append(r_m_p)
            self.list_of_weighted_meal_plans.append(weight_and_meal)
        #sort the meal plans by the weighted sum
        self.list_of_weighted_meal_plans.sort(key=lambda x: x[0])

    def display(self):
        # for item in self.list_of_weighted_meal_plans:
        #     print("Weight", item[0])
        #     for meal in item[1]:
        #         for m in meal:
        #             print(m.name)            
        #structure of list_of_weighted_meal_plans: [weight, [[bf], [lunch], [dinner]]]
        # print("Best Meal Plan")
        # print("Weight", self.list_of_weighted_meal_plans[0][0])
        for i in range(4):
            print(sum_calories_and_macros(self.list_of_weighted_meal_plans[0][1])[i])
        for meal_plan in self.list_of_weighted_meal_plans[0][1]:
            print(meal_plan)
            for meal in meal_plan:
                print(meal.name)
    def to_json(self):
        json_meal_plan = dict()
        for meal_plan in self.list_of_weighted_meal_plans:
            all_meals_in_plan = list()
            for meal_time in meal_plan[1]:
                for meal in meal_time:
                    all_meals_in_plan.append(meal.to_dict())
            json_meal_plan[meal_plan[0]] = all_meals_in_plan
        return json_meal_plan
    def calendar_to_json(self):
        json_calendar = dict()
        for meal in self.calendar:
            json_calendar[meal.name] = meal.to_dict()
        return json_calendar
    

def calculate_weights(possible_meal_plan, desired_values) -> float:
    calorie_weight = .15
    protein_weight = 2.5
    carb_weight = 1
    fat_weight = 1
    desired_calories = desired_values[0]
    desired_protein = desired_values[1]
    desired_carbs = desired_values[2]
    desired_fat = desired_values[3]
    weighted_sum = 0
    total_calories, total_protein, total_carbs, total_fat = sum_calories_and_macros(possible_meal_plan)

    caloric_difference = abs(total_calories - desired_calories)
    protein_difference = total_protein - desired_protein
    if protein_difference < 0:
        protein_difference = abs(protein_difference)/2
    carb_difference = abs(total_carbs - desired_carbs)
    fat_difference = abs(total_fat - desired_fat)
    weighted_sum += caloric_difference * calorie_weight + protein_difference * protein_weight + carb_difference * carb_weight + fat_difference * fat_weight
    return weighted_sum

def sum_calories_and_macros(meal_plan):
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    for meals in meal_plan:
        for meal in meals:
            if (meal.calories != ''):
                total_calories += int(meal.calories)
                total_protein += int(meal.protein)
                total_carbs += int(meal.carbs)
                total_fat += int(meal.fat)
    return total_calories, total_protein, total_carbs, total_fat
