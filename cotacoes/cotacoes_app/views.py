from django.views.generic.edit import FormView
from django.views.generic.detail import SingleObjectMixin
from cotacoes_app.forms import CotacaoForm
import datetime
from cotacoes_app.models import Cotacao, Currencies
# Create your views here.


class CotacaoFormView(SingleObjectMixin, FormView):
    template_name = 'cotacoes_app/index.html'
    form_class = CotacaoForm
    model = Cotacao

    def post(self, request, *args, **kwargs):
        try:
            self.object = Cotacao(data_inicial=datetime.datetime.strptime(self.request.POST['data_inicial'], '%d/%m/%Y'),
            data_final=datetime.datetime.strptime(self.request.POST['data_final'], '%d/%m/%Y'),
            moeda_a_ser_cotada=Currencies(self.request.POST['moeda_a_ser_cotada']))
        except Exception as e:
            print(e)
            self.object = Cotacao()


        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))

    def get(self, request, *args, **kwargs):
        self.object = Cotacao()
        return super().get(request, *args, **kwargs)
    