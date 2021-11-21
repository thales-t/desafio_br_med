from django.urls import path
from cotacoes_app.views import CotacaoFormView

app_name='cotacoes_app'

urlpatterns = [
    path('', CotacaoFormView.as_view(), name='index'),
]