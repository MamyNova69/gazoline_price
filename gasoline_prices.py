import requests
import pandas as pd

class gazoline_price:
    def __init__(self):
        self.url = 'https://www.prix-carburants.gouv.fr'
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

    def recupererOpenPdvs(self): # récupère les points de vente de carburant
        # la réponse est un json
        response = requests.get(f'{self.url}/map/recupererOpenPdvs/', cookies=self.cookies, headers=self.headers_to_get_datas)
        # print(response.text)
        return response.text

    def recuperer_infos_pdv(self, id_pdv): # retourn un dataframe panda
        response = requests.get(f"{self.url}/map/recuperer_infos_pdv/"+id_pdv,
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


if __name__ == '__main__':
    gaz = gazoline_price()
    # print(gaz.recupererOpenPdvs())
    html = gaz.recuperer_infos_pdv('69007006')



