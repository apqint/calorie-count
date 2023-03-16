import requests
import json

with open('../keys.txt') as file:
    content = file.read()
    key = content.split('\n')[0].split('KEY:')[1].strip()

class Food:
    def __init__(self, name, _id):
        self.name = name
        self._id = _id
        self.createNutritionalData()

    def createNutritionalData(self) -> None:
        req = requests.get(f"https://api.nal.usda.gov/fdc/v1/food/{self._id}?api_key={key}")
        data = json.loads(req.content)
        payload = {
            "calories": [data['foodNutrients'][2]['amount'], 'kcal'],
            "protein": [data['foodNutrients'][4]['amount'], "g"]
        }
        self.payload = payload

    def createFullNutritionalData(self) -> None:
        req = requests.get(f"https://api.nal.usda.gov/fdc/v1/food/{self._id}?api_key={key}")
        data = json.loads(req.content)
        payload = {}
        for i in data['foodNutrients']:
            try:
                payload[f'{i["nutrient"]["name"].lower()}'] = [i['amount'],i['nutrient']['unitName']]
            except KeyError:
                pass
        payload['calories'] = [data['foodNutrients'][2]['amount'], 'kcal']
        self.payload = payload
