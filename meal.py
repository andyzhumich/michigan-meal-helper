#defines the meal class, which consists of a name, calories, macros, and serving size
#meal class definition
class Meal:
    def __init__(self, name, calories, protein, carbs, fat, time, allergens):
        self.name = name
        self.calories = calories
        self.protein = protein
        self.carbs = carbs
        self.fat = fat
        self.time = time
        self.allergens = allergens
    def display(self):
        print(self.name)
        print(self.calories)
        print(self.protein)
        print(self.carbs)
        print(self.fat)
        print(self.time)
        print(self.allergens)


hi = "hi"
print("hello", hi)