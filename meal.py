#defines the meal class, which consists of a name, calories, macros, and serving size
#meal class definition

import random
class Meal:
    def __init__(self, name, calories, protein, carbs, fat, time, allergens, dining_hall):
        self.name = name
        self.calories = calories
        self.protein = protein
        self.carbs = carbs
        self.fat = fat
        self.time = time
        self.allergens = allergens
        self.dining_hall = dining_hall
    def display(self):
        print(self.name)
        print(self.calories)
        print(self.protein)
        print(self.carbs)
        print(self.fat)
        print(self.time)
        print(self.allergens)
        print(self.dining_hall)
for i in range(10):
    print(random.randint(0, 10))