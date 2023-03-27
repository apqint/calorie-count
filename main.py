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
    misc = [] #eaten any time
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

    def totalCals():
        total = 0
        # for i in (breakfast+lunch+dinner+misc):
            # total+=i.payload['calories']*100/i.amount
        print((breakfast+lunch)+dinner+misc)

        return total

    def searchFood():
        print(Scheme.question + " Food type: ", end="")
        queue = input("")
        print(Scheme.question + " # of results: ", end="")
        hits = int(input(""))
        try:
            results = search(hits, queue, key)
        except KeyError:
            print(Scheme.error + " Error! Likely from an invalid API key.")
        for x, i in enumerate(results):
            print(f'  {Fore.CYAN}[{x+1}]{Fore.WHITE} {i["description"]} ({i["category"]}{f""": {i["brand"]})""" if "brand" in i else ""} -> {i["calories"]} calories/100g')
        print(Scheme.question + f" What variant would you like to add? (1-{hits}): ", end="")
        nr = int(input(""))
        print(Scheme.question + f" How much? (in grams): ", end="")
        amount = int(input(""))
        food_to_add = Food(results[nr-1]['description'], results[nr-1]['id'], amount, key)
        return food_to_add

    def addFood():
        printMeals()
        print(Scheme.question + " Which meal would you like to appoint to? ", end="")
        meal = input("")
        meal = meals_pointer[meal.lower().strip()] if not meal.isdigit() else meals[int(meal)-1]
        food = searchFood()
        meal.append(food)
        print(meal)
    addFood()
    os.system('PAUSE>NUL')

if __name__=="__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        os.system('pause')
