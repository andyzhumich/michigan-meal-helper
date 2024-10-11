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
    def to_list(self):
        return [self.name, self.calories, self.protein, self.carbs, self.fat, self.time, self.allergens, self.dining_hall]
    def to_dict(self):
        return {
            'name': self.name,
            'calories': self.calories,
            'protein': self.protein,
            'carbs': self.carbs,
            'fat': self.fat,
            'time': self.time,
            'allergens': self.allergens,
            'dining_hall': self.dining_hall
        }
