# **NutriDiarium**
NutriDiarium is a simple nutrition tracker built with Python. It can help you eat better and reach your weight goals.

This is my final project for CS50's Introduction to Programming with Python.


## Table of Contents
- [Video demo](#video-demo)
- [Features](#features)
- [FAQ](#frequently-asked-questions)
- [Project struture](#project-struture)
- [Installation](#installation)
- [Usage](#Usage)

## Video Demo: https://youtu.be/UJ3MI6qSVFg

## Features
- Calculate the ideal amount of calories and macronutrients you should consume.
- Track your calories and macronutrients.
- Saves data locally in CSV files.
- Uses a simple command-line interface.


## Frequently Asked Questions
### What is IDNI? What does it mean?
- IDNI stands for Ideal Daily Nutritional Intake. It's the calories, carbohydrates, fat and protein that you should ideally consume every day.
- The values are different for every person and are based on age, height, weight, gender, how active you are through the day and your weight goal.

### How is my IDNI being calculated? What is the formula?
- To calculate the calories it uses the Mifflin St. Jeor equation, which is considered the best formula by many nutritionists.

- To calculate the macronutrients:
    - Fat = (Calories * 0.3) / 9
    - Protein = (Calories * 0.3) / 4
    - Carbohydrates* = (Calories * 0.4) / 4

### How is data being stored? Is it possible to edit it without using the program?
- The program will create 3 CSV files automatically after you open it for the first time. All data is stored in those files and you _can_ alter them in separate programs.
- If the program breaks simply delete the 3 CSV files in the directory and let the program create new ones automatically.


## Project structure
### Folder contents:
- project.py - Contains the main function and all other functions.
- requirements.txt - All required pip-installable libraries.
- test_project.py - This file contains the test functions for project.py.
### Files created after using the program:
- personal_info.csv - Stores the user's IDNI values (Ideal Daily Nutritional Intake).
- food.csv - Stores the values of the foods the user added to the database.
- date.csv - Stores the user's nutritional intake during the day.


## Installation
Download the Repository through Clone Repository or Download Zip
```
git clone https://github.com/diogo-martins18/NutriDiarium
```
After download, navigate to the project folder directory.
```
cd NutriDiarium
```
Use [pip](https://pip.pypa.io/en/stable/) to install needed libraries.
```
pip install -r requirements.txt
```

## Usage
Run the program via:
```
python3 project.py
```
If it's your first time opening the program, you will be greeted with this screen.
```
#############################
#  Welcome to NutriDiarium  #
#############################

--- Getting personal information ---
IDNI (Ideal Daily Nutritional Intake) is the amount of calories and
macronutrients that you should consume daily to achieve your weight goal.

If you don't know your IDNI values, select 'Calculate your IDNI'.
If you know your IDNI values, select 'Enter your IDNI manually'.

1: Calculate your IDNI
2: Enter your IDNI manually
Enter your choice:
```
Select the option you want and provide the values prompted by the program.

After getting your IDNI values, you can access the main menu:
```
┌─────────────────────────┐
│ MAIN MENU               │
├─────────────────────────┤
│ 1: Personal information │
│ 2: Food                 │
│ 3: Diary                │
│ Q: Quit the program     │
└─────────────────────────┘
```
To enter a food in the database, select "Food" and "Add food to database". Provide the values prompted by the program.
```
┌────────────────────────────┐
│ FOOD MENU                  │
├────────────────────────────┤
│ 1: Show food database      │
│ 2: Add food to database    │
│ 3: Edit food in database   │
│ 4: Delete food in database │
│ 5: Clear food database     │
│ B: Back to the main menu   │
└────────────────────────────┘
```

To see the whole database, select "Show food database".

```
--- Showing food database ---
┌────────┬───────────┬────────────┬───────┬─────────┬───────────┐
│ Name   │  Portion  │  Calories  │  Fat  │  Carbs  │  Protein  │
├────────┼───────────┼────────────┼───────┼─────────┼───────────┤
│ Banana │    100    │     89     │  0.3  │   23    │    1.1    │
└────────┴───────────┴────────────┴───────┴─────────┴───────────┘
```

To add food to your diary log, select "Diary" and "Add food to diary". Provide the values prompted by the program.
```
┌──────────────────────────┐
│ DIARY MENU               │
├──────────────────────────┤
│ 1: Show diary log        │
│ 2: Add food to diary log │
│ 3: Clear diary log       │
│ B: Back to the main menu │
└──────────────────────────┘
```
To see the diary, select "Show diary".
```
--- Showing today's diary ---
┌──────────┬────────────┬────────────────────┬──────────┐
│ Value    │  Consumed  │ Progress bar       │  Target  │
├──────────┼────────────┼────────────────────┼──────────┤
│ Calories │     89     │ [..........] 3.71% │   2400   │
│ Fat      │    0.3     │ [..........] 0.43% │    70    │
│ Carbs    │     23     │ [..........] 7.19% │   320    │
│ Protein  │    1.1     │ [..........] 0.73% │   150    │
└──────────┴────────────┴────────────────────┴──────────┘
```
