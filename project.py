import sys
import os
import sqlite3
import pyinputplus as pyip
import matplotlib.pyplot as plt
from tabulate import tabulate
from datetime import date


connection = sqlite3.connect("database.db")
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

IDNI_HEADER = ["Calories", "Fat", "Carbs", "Protein"]
FOOD_HEADER = ["Name", "Portion", "Calories", "Fat", "Carbs", "Protein"]
DIARY_HEADER = ["Value", "Consumed", "Progress bar", "Target"]
date = date.today()


def main():
    # Clear terminal
    os.system("clear||cls")

    # Print welcome screen
    print(
        "#############################\n"
        "#  Welcome to NutriDiarium  #\n"
        "#############################"
    )

    # Go to main menu
    main_menu()


def main_menu():
    table = [
        ["MAIN MENU"],
        ["1: Personal information"],
        ["2: Food"],
        ["3: Diary"],
        ["4: Weight progression"],
        ["Q: Quit the program"],
    ]
    print("")
    print(tabulate(table, headers="firstrow", tablefmt="simple_outline"))
    match input("Enter your choice: ").upper():
        case "1":
            personal_info_menu()
        case "2":
            food_menu()
        case "3":
            diary_menu()
        case "4":
            weight_menu()
        case "Q":
            sys.exit("Exiting program...")
        case _:
            main_menu()


######################
#   MENU FUNCTIONS   #
######################


def personal_info_menu():
    table = [
        ["1: Show IDNI"],
        ["2: Change IDNI"],
        ["B: Back to the main menu"],
    ]
    print("")
    print(tabulate(table, headers=["PERSONAL INFO MENU"], tablefmt="simple_outline"))
    match input("Enter your choice: ").upper():
        case "1":
            show_idni()
        case "2":
            new_idni()
        case _:
            main_menu()


def food_menu():
    table = [
        ["1: Show food database"],
        ["2: Add food to database"],
        ["3: Edit food in database"],
        ["4: Delete food in database"],
        ["5: Clear food database"],
        ["B: Back to the main menu"],
    ]
    print("")
    print(tabulate(table, headers=["FOOD MENU"], tablefmt="simple_outline"))
    match input("Enter your choice: ").upper():
        case "1":
            show_food_database()
            food_menu()
        case "2":
            add_food_to_database()
        case "3":
            edit_food_in_database()
        case "4":
            delete_food_in_database()
        case "5":
            clear_food_database()
        case _:
            main_menu()


def diary_menu():
    table = [
        ["1: Add food to diary"],
        ["2: Show diary"],
        ["3: Clear diary"],
        ["4: Manage diary from the past"],
        ["B: Back to the main menu"],
    ]
    print("")
    print(tabulate(table, headers=[f"DIARY MENU - {date}"], tablefmt="simple_outline"))
    match input("Enter your choice: ").upper():
        case "1":
            add_food_to_diary()
        case "2":
            show_progress()
        case "3":
            clear_diary()
        case "4":
            change_diary_date()
        case _:
            main_menu()

def weight_menu():
    table = [
        ["1: Show weight logs"],
        ["2: Add weight entry"],
        ["B: Back to the main menu"],
    ]
    print("")
    print(tabulate(table, headers=[f"WEIGHT MENU"], tablefmt="simple_outline"))
    match input("Enter your choice: ").upper():
        case "1":
            show_weight_progression()
        case "2":
            add_weight_entry()
        case _:
            main_menu()





#########################
#   SUBMENU FUNCTIONS   #
#########################


def show_idni():
    print(f"\n--- Showing IDNI ---")
    idni = cursor.execute(
        """
        SELECT calories, fat, carbs, protein FROM person_idni
        ORDER BY id DESC
        LIMIT 1
        """
    )

    print_table(idni, IDNI_HEADER)
    personal_info_menu()


def new_idni():
    # Get IDNI values from user manually or by calculating.
    match input(
        "1: Calculate your IDNI\n" "2: Enter your IDNI manually\n" "Enter your choice: "
    ):
        case "1":
            idni = calculate_idni()
        case "2":
            print("\n--- Getting IDNI values---")
            print("Introduce the IDNI values: ")
            idni = [pyip.inputNum(f"{value}: ", min=1) for value in IDNI_HEADER]
        case _:
            new_idni()

    cursor.execute(
        """
        INSERT INTO person_idni (
            insert_date,
            calories,
            fat,
            carbs,
            protein
        )
        VALUES(?, ?, ?, ?, ?)
        """,
        (date, idni[0], idni[1], idni[2], idni[3]),
    )
    connection.commit()
    personal_info_menu()


def show_food_database():
    print(f"\n--- Showing food database ---")
    food_database = cursor.execute(
        """
        SELECT name, portion, calories, fat, carbs, protein
        FROM food
        """
    )

    print_table(food_database, FOOD_HEADER)
    food_menu()


def add_food_to_database():
    print(
        "\n--- Adding food to the database ---\n"
        "Write the name of the food you want to add, the portion (in grams), and macronutrients.\n"
        "Example: Name: Banana, Portion: 100, Calories: 89, etc...\n"
        "\nEnter the food's values:"
    )

    # Ask user for information about the food they want to add.
    food_values = []
    for value in FOOD_HEADER:
        if value == "Name":
            food_values.append(pyip.inputStr("Name: "))
        else:
            food_values.append(pyip.inputNum(f"{value}: ", min=0.1))

    # Append food to food.csv.
    cursor.execute(
        """
        INSERT INTO food (name, portion, calories, fat, carbs, protein)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            food_values[0],
            food_values[1],
            food_values[2],
            food_values[3],
            food_values[4],
            food_values[5],
        ),
    )
    connection.commit()

    print(
        "\n*** Food added successfully to the database! ***\n"
        "Returning to the menu..."
    )
    food_menu()


def edit_food_in_database():
    print("\n--- Editing food in the database ---")

    # Prompts the user for the name of the food to be edited.
    food_name = input("Name of the item you want to edit: ")

    if check_if_item_exists_in_database("food", "name", food_name):
        new_item = []
        for value in FOOD_HEADER:
            if value == "Name":
                new_item.append(pyip.inputStr("New Name: "))
            else:
                new_item.append(pyip.inputNum(f"New {value}: ", min=0.1))

        cursor.execute(
            """
            UPDATE food
            SET name = ?,
            portion = ?,
            calories = ?,
            fat = ?,
            carbs = ?, 
            protein = ?
            WHERE name LIKE ?
            """,
            (
                new_item[0],
                new_item[1],
                new_item[2],
                new_item[3],
                new_item[4],
                new_item[5],
                food_name,
            ),
        )
        connection.commit()
        print("\n*** Item edited successfully! ***\n" "Returning to the menu...")

    else:
        print("The food you entered isn't in the database")
    food_menu()


def delete_food_in_database():
    print("\n--- Deleting food in the database ---")

    # Prompts the user for the name of the food to be edited.
    food_name = input("Name of the item you want to delete: ")

    if check_if_item_exists_in_database("food", "name", food_name):
        cursor.execute(
            """
            DELETE FROM food
            WHERE name LIKE ?
            """,
            ([food_name]),
        )
        connection.commit()
        print("\n*** Item deleted successfully! ***\n" "Returning to the menu...")
    else:
        print("The food you entered isn't in the database")
    food_menu()


def clear_food_database():
    print("\n--- Clearing food database ---")

    print("WARNING: This willl delete the entire food database.")
    if input("Do you still want to continue? (Y/N): ").upper() == "Y":
        cursor.execute(
            """
            DELETE FROM food
            """,
        )
        connection.commit()
        print("\n*** Food database cleared successfully! ***")

    print("\nReturning to the menu...")
    food_menu()


def show_progress():
    total = cursor.execute(
        """
        SELECT total_calories_consumed,
            total_fat_consumed,
            total_carbs_consumed,
            total_protein_consumed       
        FROM diary
        WHERE date = ?
        ORDER BY id DESC
        """,
        ([date]),
    ).fetchone()

    idni_values = cursor.execute(
        """
        SELECT calories, fat, carbs, protein
        FROM person_idni
        ORDER BY id DESC
        """
    ).fetchone()

    if total:
        diary_header = [
            "total_calories_consumed",
            "total_fat_consumed",
            "total_carbs_consumed",
            "total_protein_consumed",
        ]

        default_diary = []
        for index, value in enumerate(IDNI_HEADER):
            default_diary.append(
                {
                    "Value": value,
                    "Consumed": total[diary_header[index]],
                    "Progress bar": make_progress_bar(
                        total[diary_header[index]], idni_values[value.lower()]
                    ),
                    "Target": idni_values[value.lower()],
                }
            )

        print("\n\nShowing today's progress:")
        print_table(default_diary, "keys", skip=True)

        food_consumed = cursor.execute(
        """
        SELECT food_name, portion_consumed, calories, fat, carbs, protein 
        FROM food_consumed
        WHERE date = ?
        """,
            ([date]),
        )

        print("\nShowing the food you consumed today: ")
        print_table(food_consumed, FOOD_HEADER)

    else:
        default_diary = []
        for value in IDNI_HEADER:
            default_diary.append(
                {
                    "Value": value,
                    "Consumed": 0,
                    "Progress bar": make_progress_bar(0, idni_values[value.lower()]
                    ),
                    "Target": idni_values[value.lower()],
                }
            )

        print("\n\nShowing today's progress:")
        print_table(default_diary, "keys")

    diary_menu()


def add_food_to_diary():
    food_name = input("Type the name of the food you want to add: ")
    if check_if_item_exists_in_database("food", "name", food_name):
        portion = pyip.inputNum("Type the portion of the meal in grams: ", min=0.1)

        food = cursor.execute(
            """
            SELECT portion, calories, fat, carbs, protein
            FROM food
            WHERE name LIKE ?
            """,
            (food_name,),
        ).fetchone()

        ratio = portion / food["portion"]

        consumed_values = []
        for food_property in IDNI_HEADER:
            consumed_values.append(food[food_property.lower()] * ratio)

        cursor.execute(
        """
        INSERT INTO food_consumed(
        date, 
        food_name, 
        portion_consumed, 
        calories, 
        fat, 
        carbs, 
        protein
        )           
        VALUES(?, ?, ?, ?, ?, ?, ?);
        """,
            (
                str(date),
                food_name,
                portion,
                consumed_values[0],
                consumed_values[1],
                consumed_values[2],
                consumed_values[3],
            ),
        )
        connection.commit()

        total_consumed = cursor.execute(
            """
            SELECT SUM(calories), SUM(fat), SUM(carbs), SUM(protein)
            FROM food_consumed
            WHERE date = ?
            """,
            (date,),
        ).fetchone()

        cursor.execute(
            """
            INSERT INTO diary(
            date, 
            total_calories_consumed,
            total_fat_consumed,
            total_carbs_consumed,
            total_protein_consumed          
            )
            VALUES(?, ?, ?, ?, ?)
            """,
            (
                date,
                total_consumed["SUM(calories)"],
                total_consumed["SUM(fat)"],
                total_consumed["SUM(carbs)"],
                total_consumed["SUM(protein)"],
            ),
        )
        connection.commit()

    else:
        print("The food you entered isn't in the database.")
    diary_menu()


def clear_diary():
    print(f"\n--- Clearing diary from {date} ---", date)

    print(
        f"WARNING: This will delete the log of the food you consumed in {date}.", date
    )
    if input("Do you still want to continue? (Y/N): ").upper() == "Y":
        cursor.execute(
            """
            DELETE FROM diary
            WHERE date LIKE ?
            """,
            ([date]),
        )
        cursor.execute(
            """
            DELETE FROM food_consumed
            WHERE date LIKE ?
            """,
            ([date]),
        )
        connection.commit()
        print("\n*** Food database cleared successfully! ***")

    print("\nReturning to the menu...")
    diary_menu()


def change_diary_date():
    available_dates = cursor.execute(
        """
    SELECT DISTINCT(date)
    FROM diary;
    """
    )
    
    print_table(available_dates, ["Available dates"], skip=True)

    
    user_date = input("Choose a date from the list: ")

    if check_if_item_exists_in_database("diary", "date", user_date):
        global date
        date = user_date

    else:
        print("The date you entered isn't available.")
        print("Returning to the diary menu...")
    diary_menu()


def add_weight_entry():
    date="2024-08-22"
    weight = pyip.inputNum("Weight: ", min=1, max=999)
    try:
        cursor.execute(
            """
            INSERT INTO weight(
            date, 
            weight        
            )
            VALUES(?, ?)
            """,
            (
                str(date),
                weight,
            ),
        )
        connection.commit()
        print("\n*** Weight log added successfully to the database! ***")
    
    except sqlite3.IntegrityError:
        print("\n*** You already logged a weight today! Try tomorrow. ***")


    print("Returning to the menu...")
    weight_menu()

def show_weight_progression():
    weight_progression = cursor.execute(
        """
    SELECT *
    FROM weight;
    """
    )

    dates=[]
    weight=[]
    for row in weight_progression:
        dates.append(row["date"])
        weight.append(row["weight"])

    plt.plot(dates, weight)
    plt.title("Weight")
    plt.xlabel("Date")
    plt.ylabel("Weight")
    plt.tight_layout()
    plt.show()

    print("Returning to the menu...")
    weight_menu()

#########################
#   OTHER FUNCTIONS   #
#########################


def check_if_item_exists_in_database(table, column, item):
    cursor.execute(
        f"""
        SELECT {column} FROM {table}
        WHERE {column} LIKE ?;
        """,
        ([item])

    )

    if cursor.fetchall():
        return True
    else:
        return False


def calculate_idni() -> list:
    """
    Get user information and calculate their IDNI
    """
    print("\n--- Calculating IDNI ---")

    # Get user information
    print("Introduce the following information to calculate your IDNI: ")
    age = pyip.inputNum("Age: ", min=1, max=115)
    height = pyip.inputNum("Height in centimeters: ", min=65, max=270)
    weight = pyip.inputNum("Weight in kilograms: ", min=10, max=360)
    activity = pyip.inputNum(
        "How active are you during the day? (1-10): ", min=1, max=10
    )
    gender = pyip.inputChoice(["Male", "Female"], prompt="Gender (Male / Female): ")
    while True:
        match input(
            "1: Lose weight\n2: Maintain weight\n3: Gain weight\nEnter your choice: "
        ):
            case "1":
                goal = -500
                break
            case "2":
                goal = 0
                break
            case "3":
                goal = 500
                break
            case _:
                pass

    # Calculate activity
    activity = (activity / 10) + 1

    # Calculate ideal calories
    if gender == "Male":
        calories = (10 * weight + 6.25 * height - 5 * age + 5) * activity + goal
    elif gender == "Female":
        calories = (10 * weight + 6.25 * height - 5 * age - 161) * activity + goal

    # Calculate ideal macronutrients
    fat = (calories * 0.3) / 9
    protein = (calories * 0.3) / 4
    carbs = (calories * 0.4) / 4

    # Return a list with IDEI values
    print("\n*** IDNI calculated successfully! ***")
    print("To see your IDNI values go to the Personal information menu")
    return [round(calories), round(fat), round(carbs), round(protein)]


def make_progress_bar(consumed, target):
    percentage = round(((consumed / target) * 100), 2)

    if percentage > 100:
        bars = "=" * 10
        empty = "." * 0
    else:
        bars = "=" * int(percentage / 10)
        empty = "." * (10 - len(bars))

    return f"[{bars}{empty}] {percentage}%"


def print_table(data, header, skip=False):
    print(
        tabulate(
            data,
            headers=header,
            tablefmt="simple_outline",
            numalign="center",
        )
    )
    if not skip:
        input("Press enter to go back to the menu: ")


if __name__ == "__main__":
    main()
