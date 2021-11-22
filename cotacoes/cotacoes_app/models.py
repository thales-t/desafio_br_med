from django.db import models
import datetime
import requests
from django.core.validators import MinLengthValidator
from workalendar.america import Brazil
from datetime import date

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

    data_inicial = models.DateField(help_text="Por favor, use o seguinte formato: <em>DD/MM/YYYY</em>.")
    data_final = models.DateField(help_text="Por favor, use o seguinte formato: <em>DD/MM/YYYY</em>.")

    #Deve ser possível variar as moedas (real, euro e iene). 
    REAL = 'BRL'
    EURO = 'EUR'
    IENE = 'JPY'
    currencies = {
        (REAL, 'Real'),
        (EURO, 'Euro'),
        (IENE, 'Iene'),
    }
    moeda_base = models.CharField(max_length=3, validators=[MinLengthValidator(3)], choices=currencies,
        default=REAL,)

    def get_cotacao_entre_data_inicial_e_final(self) -> list[tuple[str, float()]]:
        """
            Retorna uma lista com as cotações, referente a cada dia entre a data inicial e final
            levando em conta a moeda base escolhida

            Returns:
                list[tuple[str, float()]]:  Um conjunto com a cotações/valores
        """
        lista_cotacao = []
        if self.data_inicial is not None and self.data_final is not None:
            cal = Brazil()
            delta = self.data_final - self.data_inicial      
            for i in range(delta.days + 1):
                day = self.data_inicial + datetime.timedelta(days=i)
                if cal.is_working_day(day):
                    lista_cotacao.append(self.get_cotacao_pela_data(day))
        return list(dict.fromkeys(lista_cotacao))

    def get_cotacao_pela_data(self, date: datetime.date) -> tuple[str, float()]:
        """
            Retorna a cotação em relação a moeda base na dada informada
        """
        payload = {'base': self.moeda_base, 'date': date.strftime('%Y-%m-%d')}
        r = requests.get('https://api.vatcomply.com/rates', params=payload).json()
        return (datetime.datetime.strptime(r['date'], '%Y-%m-%d'), r['rates']['USD'])

    
    def __init__(self, *args, **kwargs):
        super(Cotacao, self).__init__(*args, **kwargs)
        if self.data_inicial is None or self.data_final is None:
            self.data_inicial, self.data_final = Cotacao.get_data_inicial_e_final()

    @classmethod
    def get_data_inicial_e_final(cls) -> tuple[date, date]:
        """
        Retorna uma tupla para data inicial e data final iniciais 
        """
        cal = Brazil()
        data_final = date.today()
        data_inicial = cal.add_working_days(data_final , -5)
        return data_inicial, data_final

