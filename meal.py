#defines the meal class, which consists of a name, calories, macros, and serving size
#meal class definition
class Meal:
    def __init__(self, name, calories, protein, carbs, fat, serving_size, time, allergens):
        self.name = name
        self.calories = calories
        self.protein = protein
        self.carbs = carbs
        self.fat = fat
        self.serving_size = serving_size
        self.time = time
        self.allergens = allergens