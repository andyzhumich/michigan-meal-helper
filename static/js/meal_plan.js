// meal_plan.js

class mealIndexes {
    constructor() {
        var mealTimes = document.getElementsByClassName("individual-meal");
        for (var i = 0; i < mealTimes.length; i++) {
            this[mealTimes[i].id] = 0;
        }
    }
    print() {
        console.log(this);
    }
}


function initializeMealPlan(mealJson) {
    return mealJson;
}
function initializeAllMeals(allMeals) {
    console.log(allMeals);
    return allMeals;
}

function displayMealsFunction(Indexes, mealJson, override) {
    var total_nutrients = { calories: 0, protein: 0, fat: 0, carbs: 0 };
    if (Object.keys(mealJson).length > 1 || override) {
        for (const mealIndexTime in Indexes) {
            mealIndex = Indexes[mealIndexTime];
            var displayMeals = [];
            for (const meals in mealDict[mealIndex]) {
                meal = mealDict[mealIndex][meals]
                if (meal.time.toUpperCase() == mealIndexTime.toUpperCase()) {
                    displayMeals.push(meal);

                }
            }
            var caloriesAndMacros = calculateCaloriesndMacros(displayMeals);
            total_nutrients.calories += caloriesAndMacros.calories;
            total_nutrients.protein += caloriesAndMacros.protein;
            total_nutrients.fat += caloriesAndMacros.fat;
            total_nutrients.carbs += caloriesAndMacros.carbs;



            var individualMealdiv = createMealButtons(displayMeals, mealIndexTime);

            createRerollButtons(mealIndexTime, individualMealdiv);
        }
    }
    var editButton = document.querySelector(".edit-button");
    editButton.addEventListener("click", editMode);
    var totalCalories = document.querySelector(".total-calories");
    totalCalories.innerHTML = "Total Calories:<br> <span style='color: #ca9d48;'>" + total_nutrients.calories + "</span>";
    
    var totalProtein = document.querySelector(".total-protein");
    totalProtein.innerHTML = "Total Protein:<br> <span style='color: #ca9d48;'>" + total_nutrients.protein + "g</span>";
    
    var totalFat = document.querySelector(".total-fat");
    totalFat.innerHTML = "Total Fat:<br> <span style='color: #ca9d48;'>" + total_nutrients.fat + "g</span>";
    
    var totalCarbs = document.querySelector(".total-carbs");
    totalCarbs.innerHTML = "Total Carbs:<br> <span style='color: #ca9d48;'>" + total_nutrients.carbs + "g</span>";
    
    if (editBool == true) {

        editMode();
    }
}


function createMealButtons(displayMeals, mealIndexTime) {
    var mealJsonFrequency = makeFrequencyList(displayMeals);
    var individualMealdiv = document.querySelector(`#${mealIndexTime}.individual-meal`);
    var individualMeal = document.querySelector(`#${mealIndexTime}.individual-meal .meal-foods`);

    displayMealsSet = filterDuplicates(displayMeals);
    displayMealsSet.forEach(meal => {
        var wholeDiv = document.createElement("div");
        wholeDiv.classList.add("whole-div");
        individualMeal.appendChild(wholeDiv);
        var minusDiv = document.createElement("div");
        minusDiv.classList.add("minus-div");
        wholeDiv.appendChild(minusDiv);
        var mealDiv = document.createElement("div");
        wholeDiv.classList.add("meal-div");
        wholeDiv.appendChild(mealDiv);
        var plusDiv = document.createElement("div");
        plusDiv.classList.add("plus-div");
        wholeDiv.appendChild(plusDiv);

        var nutritionPanel;
        const button = document.createElement("button");
        button.classList.add("meal");
        button.innerHTML = meal.name + " (" + mealJsonFrequency[meal.name] + ")";
        mealDiv.appendChild(button);
        // console.log(meal.name);
        button.onmouseover = function () {
            nutritionPanel = createNutritionPanels(meal);
            button.appendChild(nutritionPanel);
        };
        button.addEventListener('mouseleave',
            () => {
                nutritionPanel.remove();
            });
        displayMealsSet.push(meal);
        // Add plus button
        createPlusMinusButtons(meal, plusDiv, minusDiv);
    });

    return individualMealdiv;
}


function createPlusMinusButtons(meal, plusDiv, minusDiv) {
    const plusButton = document.createElement("button");
    plusButton.classList.add("plus-button");
    plusButton.innerHTML = "+";
    plusButton.onclick = function () { plusminusButtons(meal, "plus"); };
    plusDiv.appendChild(plusButton);

    // Add minus button
    const minusButton = document.createElement("button");
    minusButton.classList.add("minus-button");
    minusButton.innerHTML = "-";
    minusButton.onclick = function () { plusminusButtons(meal, "minus"); };
    minusDiv.appendChild(minusButton);
}

function plusminusButtons(meal, state) {
    //state is whether button is plus or minus
    var mealIndex = Indexes[meal.time.toLowerCase()];

    if (state == "plus") {
        mealDict[mealIndex].push(meal);
        console.log(mealDict);
}
    else {
        mealDict[mealIndex].splice(mealDict[mealIndex].indexOf(meal), 1);
    }

    clearMeals();
    displayMealsFunction(Indexes, mealDict, true);

}
function filterDuplicates(displayMeals) {
    var uniqueMeals = [];
    for (var i = 0; i < displayMeals.length; i++) {
        var meal = displayMeals[i];
        var isDuplicate = false;
        for (var j = 0; j < uniqueMeals.length; j++) {
            if (meal.name === uniqueMeals[j].name) {
                isDuplicate = true;
                break;
            }
        }
        if (!isDuplicate) {
            uniqueMeals.push(meal);
        }
    }
    uniqueMeals.sort((a, b) => a.name.localeCompare(b.name));
    return uniqueMeals;
}
function editMode() {
    editBool = true;
    editButton = document.querySelector(".edit-button");
    editButton.innerHTML = "Done";

    setTimeout(() => {
        editButton.onclick = function () { doneEditing(); };
    }, 0);

    var plusButtons = document.getElementsByClassName("plus-button");
    var minusButtons = document.getElementsByClassName("minus-button");
    for (var i = 0; i < plusButtons.length; i++) {
        plusButtons[i].style.display = "block";
        minusButtons[i].style.display = "block";
    }
    toggleEditMenu(1);
}
function doneEditing() {
    editBool = false;
    editButton = document.querySelector(".edit-button");
    editButton.innerHTML = "Edit";
    setTimeout(() => {
        editButton.onclick = function () { editMode(); };
    }, 0);

    var plusButtons = document.getElementsByClassName("plus-button");
    var minusButtons = document.getElementsByClassName("minus-button");
    for (var i = 0; i < plusButtons.length; i++) {
        plusButtons[i].style.display = "none";
        minusButtons[i].style.display = "none";
    }
    toggleEditMenu(0);

}

function createRerollButtons(mealIndexTime, individualMealdiv) {
    const rerollButton = document.createElement("button");
    rerollButton.onclick = function () { rerollMealPlan(mealIndexTime); };
    rerollButton.innerHTML = "Reroll " + mealIndexTime.charAt(0).toUpperCase() + mealIndexTime.slice(1);
    rerollButton.id = mealIndexTime + "-reroll";
    rerollButton.classList.add("reroll-button");
    individualMealdiv.appendChild(rerollButton);
}

function clearMeals() {
    var mealTimes = document.getElementsByClassName("individual-meal");
    try {
        for (var i = 0; i < mealTimes.length; i++) {
            var individualMeal = document.querySelector(`#${mealTimes[i].id}.individual-meal .meal-foods`);
            individualMeal.innerHTML = "";
            var rerollButton = document.querySelector(`#${mealTimes[i].id}.individual-meal .reroll-button`);
            rerollButton.remove();
        }
    
        
    } catch (error) {
        console.log("No meals to clear");
        
    }

}

function createNutritionPanels(meal) {
    const foodNutrition = document.createElement("div");
    foodNutrition.classList.add("food-nutrition");
    foodNutrition.id = meal.name + "-nutrition";
    const calories = document.createElement("p");
    calories.innerHTML = "Calories: " + meal.calories;
    const protein = document.createElement("p");
    protein.innerHTML = "Protein: " + meal.protein + "g";
    const fat = document.createElement("p");
    fat.innerHTML = "Fat: " + meal.fat + "g";
    const carbs = document.createElement("p");
    carbs.innerHTML = "Carbs: " + meal.carbs + "g";
    foodNutrition.appendChild(calories);
    foodNutrition.appendChild(protein);
    foodNutrition.appendChild(fat);
    foodNutrition.appendChild(carbs);

    return foodNutrition;
}
function calculateCaloriesndMacros(mealPlan) {
    var calories = 0;
    var protein = 0;
    var fat = 0;
    var carbs = 0;
    var time = mealPlan[0].time.toLowerCase();
    mealPlan.forEach(item => {
        calories += Number(item.calories);
        protein += Number(item.protein);
        fat += Number(item.fat);
        carbs += Number(item.carbs);
    });
    nutrition_calories = document.querySelector("#" + time + "-nutrition-calories");
    nutrition_protein = document.querySelector("#" + time + "-nutrition-protein");
    nutrition_fat = document.querySelector("#" + time + "-nutrition-fat");
    nutrition_carbs = document.querySelector("#" + time + "-nutrition-carbs");
    nutrition_calories.innerHTML = "Calories:<br>" + calories;
    nutrition_protein.innerHTML = "Protein:<br>" + protein + "g";
    nutrition_fat.innerHTML = "Fat:<br>" + fat + "g";
    nutrition_carbs.innerHTML = "Carbs:<br>" + carbs + "g";

    return { calories, protein, fat, carbs };

}

function makeFrequencyList(mealPlan) {
    const frequency = {};

                mealPlan.forEach(item => {
                    // Assuming 'item' has a 'name' property you want to count
                    const key = item.name; // Use a unique property of the object
                    if (frequency[key]) {
                        frequency[key] += 1;
                    } else {
                        frequency[key] = 1;
                    }
                }
                );
        const sortedFrequency = Object.fromEntries(Object.entries(frequency).sort());
        return sortedFrequency;


    }

function rerollMealPlan(mealTime) { 
    var urlParams = new URLSearchParams(window.location.search);
    var goalCalories = urlParams.get("calories");
    var goalProtein = urlParams.get("protein");
    var goalFat = urlParams.get("fat");
    var goalCarbs = urlParams.get("carbs");

    // Weights for the nutrients
    var calorie_weight = 0.15;
    var protein_weight = 2.5;
    var carb_weight = 1;
    var fat_weight = 1;
    var number_of_mealplans = 50;

    // Initialize testIndexes and bestIndexes
    var initMealIndex = Indexes[mealTime];
    var testIndexes = { ...Indexes };
    var bestIndexes = { ...testIndexes };
    var weightedSumsandIndexes = {};
    
    console.log(mealTime);
    testIndexes[mealTime] = 0;
    console.log("Indexes", Indexes);
    console.log("Initial indexes:", testIndexes);
    for (var i = 0; i < number_of_mealplans; i++) {
        console.log("Current i:", i);
        if (initMealIndex == i) {
            console.log(initMealIndex);
            console.log("Skipping initial indexes");
            testIndexes[mealTime] += 1;
            continue;
        }
        var total_nutrients = { calories: 0, protein: 0, fat: 0, carbs: 0 };

        for (const mealIndexTime in testIndexes) {

            var mealIndex = testIndexes[mealIndexTime];
            // console.log(mealIndex);
            var displayMeals = [];
            for (const meals in mealDict[mealIndex]) {
                meal = mealDict[mealIndex][meals]
                if (meal.time.toUpperCase() == mealIndexTime.toUpperCase()) {
                    displayMeals.push(meal);
    
                }
            }
            // console.log(displayMeals);
            // console.log(mealIndex);
            // console.log(displayMeals[mealIndex]);
            var caloriesAndMacros = calculateCaloriesndMacros(displayMeals);
            total_nutrients.calories += caloriesAndMacros.calories;
            total_nutrients.protein += caloriesAndMacros.protein;
            total_nutrients.fat += caloriesAndMacros.fat;
            total_nutrients.carbs += caloriesAndMacros.carbs;
        }

        // Calculate the weighted sum
        var weightedSum = 
            calorie_weight * Math.abs(goalCalories - total_nutrients.calories) +
            protein_weight * Math.abs(goalProtein - total_nutrients.protein) +
            carb_weight * Math.abs(goalCarbs - total_nutrients.carbs) +
            fat_weight * Math.abs(goalFat - total_nutrients.fat);
        weightedSumsandIndexes[weightedSum] = { ...testIndexes };


        // Increment the index for the current  mealTime
        testIndexes[mealTime] += 1;
        
    }

    // Sort weightedSumsandIndexes
    var sortedWeightedSums = Object.keys(weightedSumsandIndexes).sort(function(a, b) {
        return a - b;
    });

    // Get the top 10 lowest weighted sums
    var lowestWeightedSums = sortedWeightedSums.slice(0, 5);
    var chosenIndex = lowestWeightedSums[Math.floor(Math.random() * lowestWeightedSums.length)];




    // Update Indexes with the chosen index
    Indexes = { ...weightedSumsandIndexes[chosenIndex] };
    // console.log("Best indexes:", bestIndexes);
    // console.log("Lowest weighted sum:", lowestWeightedSum);

    // Clear and display meals with the best indexes
    clearMeals();
    displayMealsFunction(Indexes, mealJson, false);
}

function toggleEditMenu(num) {
    var mealNameAndFoods = document.querySelectorAll(".meal-name-and-foods");
    if (num == 1) {
        document.querySelector(".add-meals").classList.remove("hidden");
        for (var i = 0; i < mealNameAndFoods.length; i++) {
            mealNameAndFoods[i].style.height = "500px";
    }
}
    else {
        document.querySelector(".add-meals").classList.add("hidden");
        for (var i = 0; i < mealNameAndFoods.length; i++) {
            mealNameAndFoods[i].style.height = "400px";
        }
    }


    }

function createEditMenu () {
    var addMeals = document.querySelector(".add-meals");
    var addMealList = document.querySelector(".add-meal-list");
    addMeals.classList.add("hidden");
        //search bar
        var searchBar = document.querySelector(".search-bar");

    //meals that have passed each filter
    var filteredMeals = [];

        //search functionality
        searchBar.addEventListener("input", function() {
            theGreatFilter();
        });
        //checkbox functionality
        var radios = document.querySelectorAll(".filter-option");
        radios.forEach(function(radio) {
            radio.addEventListener("change", function() {
                theGreatFilter();
            });
        }
        );
        // slider functionality
        $(document).ready(function() {

        $(".range").each(function() {
            var slider = $(this);
            slider.on("slide", function(event, ui) {
                if (slider.attr("id") == "cal-range") {
                    $( "#cal-amount" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
                }
                else if (slider.attr("id") == "protein-range") {
                    $( "#protein-amount" ).val( ui.values[ 0 ] + "g - " + ui.values[ 1 ] + "g" );
                }
                else if (slider.attr("id") == "fat-range") {
                    $( "#fat-amount" ).val( ui.values[ 0 ] + "g - " + ui.values[ 1 ] + "g" );
                }
                else if (slider.attr("id") == "carb-range") {
                    $( "#carb-amount" ).val( ui.values[ 0 ] + "g - " + ui.values[ 1 ] + "g" );
                }
                theGreatFilter();
            })
        });
    });


    var filterButton = document.querySelector(".filter-button");
    filterButton.innerHTML = "Filter";
    filterButton.addEventListener("click", function() {
        var filterMenu = document.querySelector(".filter-menu");
        var addMealList = document.querySelector(".add-meal-list");
        filterMenu.classList.toggle("filter-active");
        addMealList.classList.toggle("filter-active");
    });
    var mealTable = document.querySelector(".add-table-body");
    for (const meal in allMeals) {
        var mealRow = document.createElement("tr")
        mealRow.classList.add("meal-row");
        mealTable.appendChild(mealRow);
        var mealName = document.createElement("td");
        mealName.innerHTML = allMeals[meal].name;
        mealRow.appendChild(mealName);
        var mealCalories = document.createElement("td");
        mealCalories.innerHTML = allMeals[meal].calories;
        mealRow.appendChild(mealCalories);
        var mealProtein = document.createElement("td");
        mealProtein.innerHTML = allMeals[meal].protein;
        mealRow.appendChild(mealProtein);
        var mealFat = document.createElement("td");
        mealFat.innerHTML = allMeals[meal].fat;
        mealRow.appendChild(mealFat);
        var mealCarbs = document.createElement("td");
        mealCarbs.innerHTML = allMeals[meal].carbs;
        mealRow.appendChild(mealCarbs);
        var mealTime = document.createElement("td");
        mealTime.innerHTML = allMeals[meal].time;
        mealRow.appendChild(mealTime);



        mealRow.dataset.name = allMeals[meal].name;
        mealRow.dataset.calories = allMeals[meal].calories;
        mealRow.dataset.protein = allMeals[meal].protein;
        mealRow.dataset.fat = allMeals[meal].fat;
        mealRow.dataset.carb = allMeals[meal].carbs;
        mealRow.dataset.time = allMeals[meal].time;
        mealRow.onclick = function () { plusminusButtons(allMeals[meal], "plus"); };
    }
    


    function applySliderFilters(slider, filters, values) {
        var sliderId = slider.attr("id");
        // console.log(sliderId + ":   " + values);
        var macro = sliderId.split("-")[0];
        if (macro == "cal") {
            macro = "calories";
        }

        filters[macro] = values;
        //filter buttons based on slider values
        console.log(filters);
        return filters;

    }
    function theGreatFilter() {
        //search functionality
        var searchBar = document.querySelector(".search-bar");
        var search = searchBar.value.toLowerCase();
        var mealButtons = addMeals.querySelectorAll(".meal-row");
        var filteredMeals = Object.values(mealButtons);

        mealButtons.forEach(function(button) {
            var mealName = button.dataset.name.toLowerCase();
            if (!mealName.includes(search)) {
                filteredMeals = filteredMeals.filter(value => value !== button);
            }
        }
        );
        //radio functionality
        var radios = document.querySelectorAll(".filter-option");
        radios.forEach(function(radio) {
            var radioTime = radio.value.toLowerCase();
            if (radio.checked && radioTime != "all") {
                mealButtons.forEach(function(button) {
                    var mealTime = button.dataset.time.toLowerCase();
                    if (!mealTime.includes(radioTime)){
                        filteredMeals = filteredMeals.filter(value => value !== button);

                        }
                    });
            }
    });
        //slider functionality
        var filters = {};
        filters["calories"] = ($("#cal-amount").val().split(" - ")).map(value => parseInt(value));
        filters["protein"] = $("#protein-amount").val().split(" - ").map(value => parseInt(value));
        filters["fat"] = $("#fat-amount").val().split(" - ").map(value => parseInt(value));
        filters["carb"] = $("#carb-amount").val().split(" - ").map(value => parseInt(value));

        mealButtons.forEach(function(button) {
            // console.log(button.dataset["name"]);
            for (const [macro, values] of Object.entries(filters)) {
                // console.log(macro);
                // console.log(values);
                var mealValue = button.dataset[macro];
                // console.log(mealValue);
                if (mealValue < values[0] || mealValue > values[1]) {
                    // console.log("removing " + button.dataset["name"]);
                    filteredMeals = filteredMeals.filter(value => value !== button);

                }
            }

        }
        );
        
        //display filtered meals
 
        for (var i = 0; i < mealButtons.length; i++) {
            if (filteredMeals.includes(mealButtons[i])) {

                mealButtons[i].style.removeProperty("display");
            }
            else {
                mealButtons[i].style.display = "none";  
            }
        }
           

    }
}

function one_meal_check() {
    var mealTimes = document.getElementsByClassName("individual-meal");
    var numbermealTimes = Object.keys(mealTimes).length;
    if (numbermealTimes == 1) {
        var title = document.querySelector(".title");
        title.innerHTML = "Your Meal";


    }

}

function main() {
    // openFile();
}



main();