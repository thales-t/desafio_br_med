from django.db import models


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
    modea_base = models.CharField(max_length=3, validators=[MinLengthValidator(3)], choices=currencies,
        default=DOLAR,)

    def get_cotacao_entre_data_inicial_e_final(self) -> list[float]:
        """
            Retorna uma lista com as cotações, referente a cada dia entre a data inicial e final
            levando em conta a moeda base escolhida

            Returns:
                list(float):  Uma lista com a cotações/valores
        """
        ...