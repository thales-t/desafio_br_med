from django.db import models
import datetime
import requests
from django.core.validators import MinLengthValidator

class Cotacao(models.Model):
    """
        Uma classe que representa o que o usuário irá interagir na pagina inicial,
        onde irá ver e selecionar a data inicial e final do gráfico da cotação
        e tabmém poder alterar o tipo de modeada

        Inicialmente o gráfico deve conter as cotações dos últimos cinco dias úteis.
        ...

        Atributos
        ----------
        data_inicial : date
        A data inicial do intervalo a ser buscado

        data_final : date
        A data final do intervalo a ser buscado
    """

    data_inicial = models.DateField()
    data_final = models.DateField()

    #Deve ser possível variar as moedas (real, euro e iene). 
    DOLAR = 'USD'
    EURO = 'EUR'
    IENE = 'JPY'
    currencies = {
        (DOLAR, 'Dolar'),
        (EURO, 'Euro'),
        (IENE, 'Iene'),
    }
    moeda_base = models.CharField(max_length=3, validators=[MinLengthValidator(3)], choices=currencies,
        default=DOLAR,)

    def get_cotacao_entre_data_inicial_e_final(self) -> list[tuple[str, float()]]:
        """
            Retorna uma lista com as cotações, referente a cada dia entre a data inicial e final
            levando em conta a moeda base escolhida

            Returns:
                list[tuple[str, float()]]:  Um conjunto com a cotações/valores
        """
        lista_cotacao = []
        if self.data_inicial is not None and self.data_final is not None:
            delta = self.data_final - self.data_inicial      
            for i in range(delta.days + 1):
                day = self.data_inicial + datetime.timedelta(days=i)
                lista_cotacao.append(self.get_cotacao_pela_data(day))
        return list(dict.fromkeys(lista_cotacao))

    def get_cotacao_pela_data(self, date: datetime.date) -> tuple[str, float()]:
        """
            Retorna a cotação em relação a moeda base na dada informada
        """
        payload = {'base': self.moeda_base, 'date': date.strftime('%Y-%m-%d')}
        r = requests.get('https://api.vatcomply.com/rates', params=payload).json()
        return (datetime.datetime.strptime(r['date'], '%Y-%m-%d'), r['rates']['BRL'])