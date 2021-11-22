from django.db import models
import datetime
import requests
from django.core.validators import MinLengthValidator
from workalendar.america import Brazil
from datetime import date
from django.db import IntegrityError

MOEDA_BASE = 'USD'

class Currencies(models.TextChoices):
        REAL = 'BRL', ('Real')
        EURO = 'EUR', ('Euro')
        IENE = 'JPY', ('Iene')


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

        moeda_a_ser_cotada: str
        A moeda que vai ser comparada em relação ao dolar
    """

    data_inicial = models.DateField(help_text="Por favor, use o seguinte formato: <em>DD/MM/YYYY</em>.")
    data_final = models.DateField(help_text="Por favor, use o seguinte formato: <em>DD/MM/YYYY</em>.")


    moeda_a_ser_cotada = models.CharField(max_length=3, validators=[MinLengthValidator(3)], choices=Currencies.choices,
        default=Currencies.REAL,)

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
        #verifica se já tem a cotação guardada
        try: 
            cotacao_api = CotacaoAPI.objects.get(data=date, moeda_cotada=self.moeda_a_ser_cotada)

        except CotacaoAPI.DoesNotExist as err:
            #Se não existir busca na api e salva no BD
            payload = {'base': MOEDA_BASE, 'date': date.strftime('%Y-%m-%d')}
            r = requests.get('https://api.vatcomply.com/rates', params=payload).json()

            #Guardando a cotação no BD
            cotacao_api = CotacaoAPI(valor=r['rates'][self.moeda_a_ser_cotada], 
                data=datetime.datetime.strptime(r['date'], '%Y-%m-%d').date(),
                moeda_cotada= self.moeda_a_ser_cotada )
            try:    
                cotacao_api.save()
            except IntegrityError as err:
                #Já salvo no banco
                ...

        return (cotacao_api.data, cotacao_api.valor)

    
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



class CotacaoAPI(models.Model):
    """
        Uma classe que ira guardar as cotações pesquisadas pelos os usuários

        Atributos
        ----------
        data : date
        A data da cotação

        valor : float 
        Valor da cotação

        moeda_a_ser_cotada: str
        A moeda que vai ser comparada em relação ao dolar
    """
    valor = models.FloatField()
    data = models.DateField()
    moeda_cotada = models.CharField(max_length=3, validators=[MinLengthValidator(3)], choices=Currencies.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['data', 'moeda_cotada'], name='cotacao_unica_moeda_dia'),
        ]