from django.shortcuts import render

# Create your views here.
class CotacaoFormView(FormView):
    template_name = 'index.html'
    form_class = CotacaoForm
    success_url = '/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)
