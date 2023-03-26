import requests
import json


def search(hits, queue, key) -> list:
    req = requests.get(f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={key}&query={queue}")
    data = json.loads(req.content)
    payload = []
    for i in range(hits):
        current = data['foods'][i]
        calories = [item for item in current['foodNutrients'] if item['nutrientName']=='Energy'][0]['value']
        payload.append({
            "id": current['fdcId'],
            "description": current['description'].lower().title(),
            "category": current['foodCategory'],
            "calories": calories,
            })
        if "brandName" in current or "brandOwner" in current:
            payload[i]["brand"]=current['brandName'] if "brandName" in current else current['brandOwner']
            
    return payload

class Food:
    def __init__(self, name, _id, amount, key) -> None:
        self.name = name
        self._id = _id
        self.key = key
        self.amount = amount
        self.createNutritionalData()

    def createNutritionalData(self) -> None:
        req = requests.get(f"https://api.nal.usda.gov/fdc/v1/food/{self._id}?api_key={self.key}")
        data = json.loads(req.content)
        payload = {
            "calories": [data['foodNutrients'][2]['amount'], 'kcal'],
            "protein": [data['foodNutrients'][4]['amount'], "g"]
        }
        self.payload = payload

    def createFullNutritionalData(self) -> None:
        req = requests.get(f"https://api.nal.usda.gov/fdc/v1/food/{self._id}?api_key={self.key}")
        data = json.loads(req.content)
        payload = {}
        for i in data['foodNutrients']:
            try:
                payload[f'{i["nutrient"]["name"].lower()}'] = [i['amount'],i['nutrient']['unitName']]
            except KeyError:
                pass
        payload['calories'] = [data['foodNutrients'][2]['amount'], 'kcal']
        self.payload = payload
