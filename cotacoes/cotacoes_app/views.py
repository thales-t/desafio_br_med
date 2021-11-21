from django.views.generic.edit import FormView
from django.views.generic.detail import SingleObjectMixin
from cotacoes_app.forms import CotacaoForm
import datetime
from cotacoes_app.models import Cotacao
# Create your views here.


class CotacaoFormView(SingleObjectMixin, FormView):
    template_name = 'cotacoes_app/index.html'
    form_class = CotacaoForm
    model = Cotacao

    def post(self, request, *args, **kwargs):
        self.object = Cotacao(data_inicial=datetime.datetime.strptime(self.request.POST['data_inicial'], '%d/%m/%Y'),
         data_final=datetime.datetime.strptime(self.request.POST['data_final'], '%d/%m/%Y'),
         modea_base=self.request.POST['modea_base'])
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))

    def get(self, request, *args, **kwargs):
        self.object = Cotacao(data_inicial=datetime.date.today(), data_final=datetime.date.today() + datetime.timedelta(days=5))
        return super().get(request, *args, **kwargs)
    