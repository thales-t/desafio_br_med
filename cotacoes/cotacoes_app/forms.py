from django import forms
from datetime import date, timedelta
from django.forms import ModelForm
from cotacoes_app.models import Cotacao
from workalendar.america import Brazil

class CotacaoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(CotacaoForm, self).__init__(*args, **kwargs)

        self.fields['data_inicial'].initial, self.fields['data_final'].initial= Cotacao.get_data_inicial_e_final()

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


    def clean(self):
        cleaned_data = super(CotacaoForm, self).clean()
        erro = []
        if cleaned_data.get('data_inicial') is None or cleaned_data.get('data_final') is None:
            raise forms.ValidationError('A data inicial e final tem que estar definida!')

        if cleaned_data['data_inicial'] >  cleaned_data['data_final']:
            self._errors['data_inicial'] = self.error_class(
                ['A data inicial não pode ser maior que a data final!']
                )

            self._errors['data_inicial'] = self.error_class(
                ['A data inicial não pode ser maior que a data final!']
                )
            erro.append(
                forms.ValidationError(('A data inicial não pode ser maior que a data final!'),
                 code='intervalo_invalido'))

        cal = Brazil()
        
        if cal.get_working_days_delta(cleaned_data['data_inicial'], cleaned_data['data_final'], include_start = True) > 5:
            self._errors['data_inicial'] = self.error_class(
                ['O período entre data inicial e final tem que ser de no máximo 5 dias úteis!']
                )

            self._errors['data_final'] = self.error_class(
                ['O período entre data inicial e final tem que ser de no máximo 5 dias úteis!']
                )
            erro.append(forms.ValidationError(
                ('O período entre data inicial e final tem que ser de no máximo 5 dias úteis!'),
                 code='max_dias_uteis'
                )
            )

        if erro:
            raise forms.ValidationError(erro)

        return cleaned_data


    class Meta:
        model = Cotacao
        fields = '__all__'