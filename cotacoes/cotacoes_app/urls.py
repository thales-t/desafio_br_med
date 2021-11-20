from django.urls import path

urlpatterns = [
    path('/', CotacaoFormView.as_view(), name='index'),
]