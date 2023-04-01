from src.food import Food, search, Meal
from colorama import Fore
from colorama import init as coloramaInit
import traceback
import os, requests
import getpass
coloramaInit()
os.system('title Calorie Counter')
class Scheme:
    question = f"{Fore.YELLOW}[?]{Fore.WHITE}"
    warning = f"{Fore.RED}[!]{Fore.WHITE}"
    affirmation = f'{Fore.GREEN}[+]{Fore.WHITE}'
    bold = '\033[1m'
    regular = '\033[0m'

key = [None]
def main():
    os.system('cls')
    breakfast = Meal("Breakfast") # eaten in the morning
    lunch = Meal("Lunch") # eaten in the afternoon
    dinner = Meal("Dinner")# eaten in the evening
    meals = [breakfast, lunch, dinner]
    meals_pointer = {
        "breakfast": breakfast,
        "lunch": lunch,
        "dinner": dinner
    }
    def tag():
        print(f"""{Fore.RED}
_________ _________  
\_   ___ \\_   ___  \ {Fore.WHITE}
/    \  \//    \  \/ 
\     \___\     \____{Fore.BLUE}
 \______  /\______  /
        \/        \/ 
            """)
    def getKey():
        print(Scheme.question + " USDA KEY ('GET' TO GET AN API KEY): ", end = "")
        key_ = input("")
        # validate key
        if key_.strip().lower()=='get': 
            os.system('start https://open.fda.gov/apis/authentication/')
            return getKey()
        print(Scheme.affirmation + " Validating...")
        req = requests.get(f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={key_}&query=tea')
        if "error" in str(req.content):
            os.system('cls')
            tag()
            print(Scheme.warning + " Invalid API Key!")
            return getKey()
        key[0] = key_
        os.system('CLS')

    def printMeals():  
        print(Scheme.affirmation + " Meals:")
        for i, x in enumerate(meals):
            print(f'  {Fore.CYAN}[{i+1}]{Fore.WHITE} {x.getName()}')

    def totalCals(meal=None):
        total = 0
        if meal == None:
            meal = []
            for i in meals:
                meal+=i.getFoods()
        for i in meal:
            total+=i.calories*i.amount/100
        return total

    def searchFood():
        print(Scheme.question + " Food type: ", end="")
        queue = input("")
        print(Scheme.question + " # of results: ", end="")
        hits = int(input(""))
        try:
            results = search(hits, queue, key[0])
        except KeyError:
            traceback.print_exc()
            print(Scheme.warning + " Error! Likely from an invalid API key.")
        for x, i in enumerate(results):
            print(f'  {Fore.CYAN}[{x+1}]{Fore.WHITE} {i["description"]} ({i["category"]}{f""": {i["brand"]}""" if "brand" in i else ""}) -> {i["calories"]} calories/100g')
        print(Scheme.question + f" What variant would you like to add? (1-{hits}): ", end="")
        nr = int(input(""))
        print(Scheme.question + f" How much? (in grams): ", end="")
        amount = int(input(""))
        food_to_add = Food(results[nr-1]['description'], results[nr-1]['id'], amount, key[0], [results[nr-1]['calories'], results[nr-1]['protein']])
        return food_to_add 

    def addFood():
        printMeals()
        print(Scheme.question + " Which meal would you like to appoint to? (0 to cancel): ", end="")
        meal = input("")
        if meal.strip() == "0": return
        try:
            meal = meals_pointer[meal.lower().strip()] if not meal.isdigit() else meals[int(meal)-1]
        except (KeyError, IndexError):
            os.system('CLS')
            tag()
            print(Scheme.bold + Scheme.warning + " No such meal." + Scheme.regular)
            return addFood()
        food = searchFood()
        meal.append(food)
        os.system("CLS")
        tag()
        print(Scheme.bold + Scheme.affirmation + f" Added {food.name} to your diet." + Scheme.regular)

    def removeFood(meal=None):
        if meal == None:
            printMeals()
            print(Scheme.question + " Which meal would you like to remove from? (0 to cancel): ", end="")
            meal = input("")
            if meal.strip() == "0": return
            meal = meals_pointer[meal.lower().strip()] if not meal.isdigit() else meals[int(meal)-1]
        foods = meal.getFoods()
        if len(foods) == 0:
            os.system('CLS')
            tag()
            print(Scheme.warning + " Nothing to remove.")
            return removeFood()
        os.system('CLS')
        tag()
        for i, x in enumerate(foods):
            print(f"{Fore.CYAN}[{i+1}]{Fore.WHITE} {x.name.split(',')[0].strip()}")
        print(Scheme.question+ " Which item would you like to remove? (int) ", end="")
        nr = int(input(""))
        food_name = foods[nr-1]
        meal.pop(nr-1)
        print(Scheme.affirmation + f" Removed {food_name.name} from {meal.getName()}.")

    def printDetailedMeals():
        for i in meals:
            foods = i.getFoods()
            print(Scheme.affirmation + f' {i.getName()} ({totalCals(foods)} calories): ')
            for i, food in enumerate(foods):
                print(f"  {Fore.CYAN}[{i+1}] {food.amount}g {food.name.split(',')[0].strip()}: {food.calories*food.amount/100} calories")
        print(Scheme.affirmation + f" Total: {totalCals()} calories")

    def createMeal():
        print(Scheme.question + " What would your meal be called? ('exit' to cancel): ", end="")
        name = input('').strip()
        if name.lower() == 'exit': return
        temp_meal = Meal(name)
        meals.append(temp_meal)
        meals_pointer[name.lower()] = temp_meal
        del temp_meal

    def removeMeal(meal=None):
        if meal==None:
            print(Scheme.question + " Which meal would you like to remove? (0 to cancel): ")
            printMeals()
            print(Scheme.question + " ", end="")
            nr = input("")
            if nr.strip() == "0": return
            try:
                meal = meals_pointer[nr.lower().strip()] if not nr.isdigit() else meals[int(nr)-1]
            except (KeyError, IndexError):
                os.system('CLS')
                tag()
                print(Scheme.bold + Scheme.warning + " No such meal." + Scheme.regular)
                return removeMeal()
        meals.remove(meal)
        print(Scheme.affirmation+ f" Removed {meal.getName()}")

    def renameMeal(meal=None):
        if meal==None:
            print(Scheme.question + " Which meal do you want do rename? (0 to cancel)")
            printMeals()
            print(Scheme.question + " ", end="")
            nr = input("")
            if nr.strip()=='0': return
            try:
                meal = meals_pointer[nr.lower().strip()] if not nr.isdigit() else meals[int(nr)-1]
            except (KeyError, IndexError):
                os.system('CLS')
                print(Scheme.bold + Scheme.warning + " No such meal." + Scheme.regular)
                return renameMeal()
        print(Scheme.question + " What should the name be? ", end="")
        name = input("")
        meal.setName(name)

    def editMeal():

        print(Scheme.question + " Which meal do you want to edit? (0 to cancel)")
        printMeals()
        print(Scheme.question + " ", end="")
        nr = input("")
        if nr.strip()=='0': return
        try:
            meal = meals_pointer[nr.lower().strip()] if not nr.isdigit() else meals[int(nr)-1]
        except (KeyError, IndexError):
            os.system('CLS')
            tag()
            print(Scheme.bold + Scheme.warning + " No such meal." + Scheme.regular)
            return editMeal()
        os.system('cls')
        tag()
        print(Scheme.affirmation + " Editing " + Scheme.bold + meal.getName() + Scheme.regular)
        actions = ["Remove from meal", "Rename meal", "Delete meal"]
        action_function = [removeFood, renameMeal, removeMeal]
        print(Scheme.affirmation + " Options:")
        for i, action in enumerate(actions):
            print(f'  {Fore.CYAN}[{i+1}] {Fore.WHITE}{action}')
        print(Scheme.question + " ", end="")
        nr = int(input(""))
        func = action_function[nr-1]
        func(meal)

    def menu():
        tag()
        actions = ["Add to meal", "Edit a meal", "Display diet", "Create meal", "Change USDA Key"]
        action_function = [addFood, editMeal, printDetailedMeals, createMeal, getKey]
        print(Scheme.affirmation + " Options:")
        for i, action in enumerate(actions):
            print(f'  {Fore.CYAN}[{i+1}] {Fore.WHITE}{action}')
        print(Scheme.question + " ", end="")
        nr = int(input(""))
        func = action_function[nr-1]
        os.system('cls')
        tag()
        func()
        print('\n' + Scheme.affirmation + Scheme.bold + " Press ENTER to return to menu." + Scheme.regular)
        ignore = getpass.getpass('')
        os.system('cls')
        menu()
    getKey()
    menu()

    os.system('PAUSE>NUL')

if __name__=="__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        os.system('pause')
