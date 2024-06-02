import requests
import pandas as pd
from math import cos, asin, sqrt
import json

# note for english readers: pdv = point de vente (french for seller)

class gazoline_france:
    def __init__(self):
        self.carburants = ["Gazole (B7)", "E85 (E85)", "SP95-E10 (E10)", "SP98 (E5)"]
        self.url = 'https://www.prix-carburants.gouv.fr' # careful with / at the end of the url
        self.headers_to_get_cookies = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
            'Accept': '*/*',
            'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            'Referer': self.url,
            'x-requested-with': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Priority': 'u=4',
        }
        self.headers_to_get_datas = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
            'Accept': '*/*',
            'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            'Referer': self.url,
            'x-requested-with': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Priority': 'u=4',
        }
        response = requests.get(self.url, headers=self.headers_to_get_cookies)
        self.cookies = response.cookies.get_dict()

    def find_sellers(self): # récupère les points de vente de carburant
        # la réponse est un json
        response = requests.get(f'{self.url}/map/recupererOpenPdvs/', cookies=self.cookies, headers=self.headers_to_get_datas)
        # print(response.text)
        return response.text

    def prices(self, id_pdv): # retourn un dataframe panda
        response = requests.get(f"{self.url}/map/recuperer_infos_pdv/"+str(id_pdv),
            cookies=self.cookies,
            headers=self.headers_to_get_datas,
        )
        html = response.text

        # load html into panda dataframe
        df = pd.read_html(html)
        # delete empty rows
        df = df[0].dropna()
        print(df)
        return df
    
    def find_closest_seller(self, lat, lon): # return the id of the closest seller to the given point
        # en utilisant la formule de haversine
        # https://fr.wikipedia.org/wiki/Formule_de_haversine
        # a simple euclidean distance would be enough for small distances assuming earth is a plane, but for the sport and beauty we use haversine
        # also someday we will run out of oil and we will need to know the distance between two points on the earth
        
        your_location = {'coordLatitude': lat, 'coordLongitude': lon}

        tempDataList = self.find_sellers()
        dictionary = json.loads(tempDataList)

        def distance(lat1, lon1, lat2, lon2):
            p = 0.017453292519943295
            haversin = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
            return 12742 * asin(sqrt(haversin))
        
        def closest(data, v):
            return min(data, key=lambda p: distance(float(v['coordLatitude']),float(v['coordLongitude']),float(p['coordLatitude']),float(p['coordLongitude'])))
        
        seller_info = closest(dictionary, your_location)

        print(f"The closest seller to your point is : {seller_info}")
        return seller_info['id']



if __name__ == '__main__':
    gaz = gazoline_france()

    id = gaz.find_closest_seller(45.740134, 4.838413)

    prix = gaz.prices(id)

    print(prix)




