from requests import get
from json import loads


def search(hits, queue, key) -> list:
    req = get(f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={key}&query={queue}&pageSize={hits}")
    data = loads(req.content)
    payload = []
    for i in range(hits):
        current = data['foods'][i]
        try: calories = [item for item in current['foodNutrients'] if item['nutrientName']=='Energy' and item['unitName'].lower()=="kcal"][0]['value']
        except: calories = 0
        try: protein = [item for item in current['foodNutrients'] if item['nutrientName']=='Protein' and item['unitName'].lower()=="g"][0]['value']
        except: protein = 0
        payload.append({
            "id": current['fdcId'],
            "description": current['description'].lower().title(),
            "category": current['foodCategory'],
            "calories": calories,
            "protein": protein
            })
        if "brandName" in current or "brandOwner" in current:
            payload[i]["brand"]=current['brandName'] if "brandName" in current else current['brandOwner']
            
    return payload

class Food:
    def __init__(self, name, _id, amount, key, nutrition) -> None:
        self.name = name
        self._id = _id
        self.key = key
        self.amount = amount
        self.calories = nutrition[0] # PER 100g
        self.protein = nutrition[1] # PER 100g, CALCULATIONS DONE LATER

    def createNutritionalData(self) -> None:
        req = get(f"https://api.nal.usda.gov/fdc/v1/food/{self._id}?api_key={self.key}")
        data = loads(req.content)
        payload = {
            "calories": [data['foodNutrients'][2]['amount'], 'kcal'],
            "protein": [data['foodNutrients'][4]['amount'], "g"]
        }
        self.payload = payload

    def createFullNutritionalData(self) -> None:
        req = get(f"https://api.nal.usda.gov/fdc/v1/food/{self._id}?api_key={self.key}")
        data = loads(req.content)
        payload = {}
        for i in data['foodNutrients']:
            try:
                payload[f'{i["nutrient"]["name"].lower()}'] = [i['amount'],i['nutrient']['unitName']]
            except KeyError:
                pass
        payload['calories'] = [data['foodNutrients'][2]['amount'], 'kcal']
        self.payload = payload

class Meal:
    def __init__(self, name):
        self.name = name
        self.food_list = []

    def append(self, thing):
        self.food_list.append(thing)

    def pop(self, thing):
        self.food_list.pop(thing)

    def setName(self, new_name):
        self.name = new_name

    def getFoods(self):
        return self.food_list

    def getName(self):
        return self.name
