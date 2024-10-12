from flask import Flask, request, render_template, redirect, url_for, session
from scanner_module import Scanner
from planner import Planner, UserPreferences
import json
app = Flask(__name__)
app.secret_key = 'super secret key'

@app.route('/')
def go_home():

    return render_template('home.html')


# http://127.0.0.1:5000/meal-plan/?calories=2500&meal-type=breakfast&meal-type=lunch&meal-type=dinner&dining-halls=Twigs&protein=100&fat=100&carbs=400


# @app.route('/submit/<items>', methods=['GET'])
# def planner(items):
#     items = request.args.get('items')  # Get the 'items' parameter from the URL
#     if items:
#         print(items)
#         return f'Items: {items}'
#     else:
#         return 'No items provided'

@app.route('/planner.html')
def go_planner():  # Add items as a parameter to the function

    return render_template('planner.html')

@app.route('/meal-plan/', methods=['GET', 'POST'])
def meal_plan():
    session['breakfast_index'] = 0
    session['brunch_index'] = 0
    session['lunch_index'] = 0
    session['dinner_index'] = 0
    if request.method == 'GET':
        calories = request.args.get('calories') 
        protein = request.args.get('protein')
        fat = request.args.get('fat')
        carbs = request.args.get('carbs')
        meal_type = request.args.getlist('meal-type')
        dining_halls = request.args.getlist('dining-halls')
        allergens = request.args.getlist('allergens')
        # print(calories, protein, fat, carbs, meal_type, dining_halls, allergens)
    scanner = Scanner()
    scanner.scan(dining_halls, meal_type)
    user_pref = UserPreferences(calories, protein, carbs, fat, allergens, meal_type, dining_halls)
    planner = Planner(scanner.calendar, user_pref)
    planner.filter()
    planner.make_meal_plan(50)
    # planner.display()

    with open('meal_plans.json', 'w') as f:
        json.dump(planner.to_json(), f, indent=4)

    # meal_type_indices = []
    # list_of_displayed_meals = []
    # for meal in meal_type:
    #     if meal:
    #         meal_type_indices.append(session[f'{meal}_index'])
    # # print(meal_type_indices)
    # for i in range(user_pref.number_of_meals):
    #     list_of_displayed_meals.append(planner.list_of_weighted_meal_plans[meal_type_indices[i]][1][i])
    return render_template('meal_plan.html', 
                           meal_types = meal_type,
                           meal_json = planner.to_json(),
                           all_meals = planner.calendar_to_json()
                           )
                        #    meal_plan = make_frequency_list(list_of_displayed_meals),)

#will crash if meal timde i snot in the list


if __name__ == '__main__':
    app.run(debug=True)


