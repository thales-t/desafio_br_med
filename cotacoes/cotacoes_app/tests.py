#from django.test import TestCase
from django.test import TestCase
import requests
from cotacoes_app.models import Cotacao
from datetime import datetime

# Create your tests here.


class TestCotacaoApp(TestCase):
    cotacao = None
    r = None
    
    def setUp(self):
        data_inicial = datetime.strptime('2020-04-06', '%Y-%m-%d')
        data_final = datetime.strptime('2020-04-10', '%Y-%m-%d')
        self.cotacao = Cotacao(data_inicial=data_inicial, data_final=data_final)

        self.r = requests.get('https://api.vatcomply.com/rates', params={'base': 'USD', 'date': '2020-04-06'})
        """
        {'date': '2020-04-06', 'base': 'USD',
        'rates': {'EUR': 0.9266981744045965, 'USD': 1.0, 'JPY': 108.92410341951627,
        'BGN': 1.8124362895005097, 'CZK': 25.579649708090077,
        'DKK': 6.918728570104717, 'GBP': 0.8136409971272357,
        'HUF': 338.4672412195348, 'PLN': 4.2297284774349,
        'RON': 4.479195625984617, 'SEK': 10.174033917153183,
        'CHF': 0.9785932721712539, 'ISK': 144.10156611991476,
        'NOK': 10.552775461032342, 'HRK': 7.06653692892225,
        'RUB': 76.43499212306551, 'TRY': 6.777499768325457,
        'AUD': 1.648596052265777, 'BRL': 5.287369103882865,
        'CAD': 1.4159948104902234, 'CNY': 7.091001760726532,
        'HKD': 7.75192289871189, 'IDR': 16412.501158372717,
        'ILS': 3.6274673338893524, 'INR': 76.0874803076638,
        'KRW': 1228.8388471874712, 'MXN': 25.10388286535076,
        'MYR': 4.364470391993327, 'NZD': 1.6865906774163657,
        'PHP': 50.659809100176076, 'SGD': 1.4345287739783155,
        'THB': 32.85979056621259, 'ZAR': 18.861458622926513}}
        """
        ...

    def tearDown(self):
        ...

    def test_conexao_api(self):
        self.assertEqual(self.r.status_code, 200)

    def test_get_cotacao_pela_data(self):
        cotacao_brl = self.cotacao.get_cotacao_pela_data(date = self.cotacao.data_inicial)
        self.assertEqual(cotacao_brl, ('2020-04-06', 5.287369103882865))


    def test_get_cotacao_entre_data_inicial_e_final(self):
        cotacoes_brl = self.cotacao.get_cotacao_entre_data_inicial_e_final()
        self.assertListEqual(cotacoes_brl,
         [('2020-04-06', 5.287369103882865), ('2020-04-07',5.206982085438677), ('2020-04-08', 5.219483028240273),
          ('2020-04-09', 5.149167203460017), ('2020-04-09', 5.149167203460017)])


if __name__ == '__main__':
    unittest.main()