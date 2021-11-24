from django.test import TestCase
import requests
from cotacoes_app.models import Cotacao, CotacaoApi
from datetime import datetime
from os import environ
from requests.auth import HTTPBasicAuth
from rest_framework.test import RequestsClient
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User

# Create your tests here.
class TestCotacaoApp(TestCase):
    cotacao = None
    r_vatcomply = None
    r_api = None
    client = None
    
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        data_inicial = datetime.strptime('2020-04-06', '%Y-%m-%d')
        data_final = datetime.strptime('2020-04-10', '%Y-%m-%d')
        cls.cotacao = Cotacao(data_inicial=data_inicial, data_final=data_final)

        CotacaoApi.objects.create(data='2020-04-06', moeda_cotada='BRL', valor=5.287369103882865)
        CotacaoApi.objects.create(data='2020-04-07', moeda_cotada='BRL', valor=5.206982085438677)
        CotacaoApi.objects.create(data='2020-04-08', moeda_cotada='BRL', valor=5.219483028240273)
        CotacaoApi.objects.create(data='2020-04-09', moeda_cotada='BRL', valor=5.149167203460017)
        CotacaoApi.objects.create(data='2020-04-14', moeda_cotada='BRL', valor=5.1614521572562255)


        User.objects.create_superuser(
            username='admin', password='admin')
        #cls.client = RequestsClient()
        cls.client = APIClient()
        cls.client.login(username='admin', password='admin')
        #cls.client.auth = HTTPBasicAuth('admin', 'admin')
        # cls.client.headers.update({'x-test': 'true'})

        cls.r_api = requests.get('https://api.vatcomply.com/rates', 
        params={'moeda_cotada': 'BRL', 'data': '2020-04-06'})

        cls.r_vatcomply = requests.get('https://api.vatcomply.com/rates',
         params={'base': 'USD', 'date': '2020-04-06'})
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
        



    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        data_inicial = datetime.strptime('2020-04-06', '%Y-%m-%d')
        data_final = datetime.strptime('2020-04-14', '%Y-%m-%d')
        self.cotacao = Cotacao(data_inicial=data_inicial, data_final=data_final)

        #self.client = RequestsClient()
        # self.client.auth = HTTPBasicAuth('admin', 'admin')
        # self.client.headers.update({'x-test': 'true'})
        self.client = APIClient()
        self.client.login(username='admin', password='admin')


        self.r_api = requests.get('https://api.vatcomply.com/rates', 
        params={'moeda_cotada': 'BRL', 'data': '2020-04-06'})

        self.r_vatcomply = requests.get('https://api.vatcomply.com/rates',
         params={'base': 'USD', 'date': '2020-04-06'})
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
        

    def test_get_first_data(self):
        cotacaoapi = CotacaoApi.objects.get(id=1)
        self.assertEqual(cotacaoapi.valor, 5.287369103882865)
        self.assertEqual(cotacaoapi.data.strftime('%Y-%m-%d'), '2020-04-06')
        self.assertEqual(cotacaoapi.moeda_cotada, 'BRL')


    def test_conexao_api_vatcomply (self):
        self.assertEqual(self.r_vatcomply.status_code, 200)

    def test_conexao_api (self):
        self.assertEqual(TestCotacaoApp.r_api.status_code, 200)

    # def test_get_cotacao_pela_data(self):
    #     cotacao_brl = self.cotacao.get_cotacao_pela_data(date = datetime.strptime('2020-04-06', '%Y-%m-%d'))
    #     print(f"{cotacao_brl} xxxxxxcotacaobrl")
    #     self.assertEqual(cotacao_brl, (datetime.strptime('2020-04-06', '%Y-%m-%d').date(), 5.287369103882865))

    # def test_get_cotacao_entre_data_inicial_e_final(self):
    #     self.cotacao.data_inicial = datetime.strptime('2020-04-06', '%Y-%m-%d')
    #     self.cotacao.data_final = datetime.strptime('2020-04-14', '%Y-%m-%d')


    #     cotacoes_brl = self.cotacao.get_cotacao_entre_data_inicial_e_final()
    #     self.assertListEqual(cotacoes_brl,
    #      [('2020-04-06', 5.7056), ('2020-04-07', 5.6678), ('2020-04-08', 5.6741),
    #       ('2020-04-09', 5.5956), ('2020-04-14', 5.6585)])

    def test_get_api(self):
        self.client = APIClient()
        self.client.login(username='admin', password='admin')
        #print(f"{self.client.auth.username} 1cliente xxxxxxxxxxzzzzzz")
        # self.client.auth = HTTPBasicAuth('admin', 'admin')
        # self.client.headers.update({'x-test': 'true'})


        response = self.client.get(f"{environ['URL_API']}"'cotacaoapi/1/')
        self.assertEqual(response.data, {'id': 1, 'valor': 5.287369103882865, 'data': '2020-04-06', 'moeda_cotada': 'BRL'})

    
    def test_post_api(self):
        """
        Garantir que foi creado um objeto da CotacaoApi
        """

        url = f"{environ['URL_API']}cotacaoapi/"
        data = {'data': '2021-11-28', 'moeda_cotada': str(self.cotacao.moeda_a_ser_cotada),
         'valor': 6.23}

        # self.client = RequestsClient()
        # self.client.auth = HTTPBasicAuth('admin', 'admin')
        # self.client.headers.update({'x-test': 'true'})
        self.client.login(username='admin', password='admin')
        # self.client.force_login(
        #     user=User.objects.first(),
        #     backend='django.contrib.auth.backends.ModelBackend' # one of your AUTHENTICATION_BACKENDS
        # )

        response = self.client.post(f"{environ['URL_API']}cotacaoapi/", data, format='json')
        import pdb; pdb.set_trace()
        print(response.request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #self.assertEqual(CotacaoApi.objects.count(), 6)
        self.assertEqual(response.data['data'], '2021-11-28')



if __name__ == '__main__':
    unittest.main()