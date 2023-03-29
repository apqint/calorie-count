from src.food import Food, search
from colorama import Fore
from colorama import init as coloramaInit
import traceback
import os
coloramaInit()
class Scheme:
    question = f"{Fore.YELLOW}[?]{Fore.WHITE}"
    warning = f"{Fore.RED}[!]{Fore.WHITE}"
    affirmation = f'{Fore.GREEN}[+]{Fore.WHITE}'
def main():
    # print(f'{Scheme.question} USDA KEY: ', end="")
    key = "BqSIVCRVNcM6FTTgS0c4GlqT4CiaFdPHwaAadj4n"#input("").strip()
    os.system('cls')
    breakfast = [] # eaten in the morning
    lunch = [] # eaten in the afternoon
    dinner = [] # eaten in the evening
    misc = [] # eaten any time
    meals = [breakfast, lunch, dinner, misc]
    meals_pointer = {
        "breakfast": breakfast,
        "lunch": lunch,
        "dinner": dinner,
        "misc": misc
    }
    def printMeals():  
        print(Scheme.affirmation + " Meals:")
        for i, x in enumerate(meals):
            print(f'  {Fore.CYAN}[{i+1}]{Fore.WHITE} {list(meals_pointer.keys())[i].title()}')

    def totalCals(meal=None):
        total = 0
        if meal == None: meal = breakfast+dinner+lunch+misc
        for i in meal:
            total+=i.calories*i.amount/100
        return total

    def searchFood():
        print(Scheme.question + " Food type: ", end="")
        queue = input("")
        print(Scheme.question + " # of results: ", end="")
        hits = int(input(""))
        try:
            results = search(hits, queue, key)
        except KeyError:
            print(Scheme.warning + " Error! Likely from an invalid API key.")
        for x, i in enumerate(results):
            print(f'  {Fore.CYAN}[{x+1}]{Fore.WHITE} {i["description"]} ({i["category"]}{f""": {i["brand"]}""" if "brand" in i else ""}) -> {i["calories"]} calories/100g')
        print(Scheme.question + f" What variant would you like to add? (1-{hits}): ", end="")
        nr = int(input(""))
        print(Scheme.question + f" How much? (in grams): ", end="")
        amount = int(input(""))
        food_to_add = Food(results[nr-1]['description'], results[nr-1]['id'], amount, key, [results[nr-1]['calories'], results[nr-1]['protein']])
        return food_to_add

    def addFood():
        printMeals()
        print(Scheme.question + " Which meal would you like to appoint to? ", end="")
        meal = input("")
        meal = meals_pointer[meal.lower().strip()] if not meal.isdigit() else meals[int(meal)-1]
        food = searchFood()
        meal.append(food)
        os.system("CLS")
        print(Scheme.affirmation + f" Added {food.name} to your diet.")

    def removeFood():
        printMeals()
        print(Scheme.question + " Which meal would you like to remove from? ", end="")
        meal = input("")
        meal = meals_pointer[meal.lower().strip()] if not meal.isdigit() else meals[int(meal)-1]
        os.system('CLS')
        for i, x in enumerate(breakfast):
            print(f"{Fore.CYAN}[{i+1}{Fore.WHITE}] {x.name.split(',')[0].strip()}")
        print(Scheme.question+ " Which item would you like to remove? (int) ")
        nr = int(input(""))
        food_name = meal[nr-1]
        meal.pop(nr-1)
        print(Scheme.affirmation + f" Removed {food_name.name} from your diet.")
        
    def printDetailedMeals():
        # breakfast
        print(Scheme.affirmation + f" Breakfast ({totalCals(breakfast)} calories):")
        for i, x in enumerate(breakfast):
            print(f"  {Fore.CYAN}[{i+1}] {x.amount}g {x.name.split(',')[0].strip()}: {x.calories*x.amount/100} calories")

        # lunch
        print(Scheme.affirmation + f" Lunch ({totalCals(lunch)} calories):")
        for i, x in enumerate(lunch):
            print(f"  {Fore.CYAN}[{i+1}] {x.amount}g {x.name.split(',')[0].strip()}: {x.calories*x.amount/100} calories")

        # dinner
        print(Scheme.affirmation + f" Dinner ({totalCals(dinner)} calories):")
        for i, x in enumerate(dinner):
            print(f"  {Fore.CYAN}[{i+1}] {x.amount}g {x.name.split(',')[0].strip()}: {x.calories*x.amount/100} calories")

        # misc
        print(Scheme.affirmation + f" Miscellaneous ({totalCals(misc)} calories):")
        for i, x in enumerate(misc):
            print(f"  {Fore.CYAN}[{i+1}] {x.amount}g {x.name.split(',')[0].strip()}: {x.calories*x.amount/100} calories")

        print(Scheme.affirmation + f" Total: {totalCals()} calories")

    def menu():
        pass
    addFood()
    addFood()
    removeFood()
    printDetailedMeals()

    os.system('PAUSE>NUL')

if __name__=="__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        os.system('pause')
