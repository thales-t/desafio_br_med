from django import forms
from datetime import date, timedelta
from django.forms import ModelForm
from cotacoes_app.models import Cotacao
from workalendar.america import Brazil

class CotacaoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(CotacaoForm, self).__init__(*args, **kwargs)

        self.fields['data_inicial'].initial = date.today()
        self.fields['data_final'].initial = date.today() + timedelta(days=5)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


    def clean(self):
        cleaned_data = super(CotacaoForm, self).clean()

        if cleaned_data.get('data_inicial') is None or cleaned_data.get('data_final') is None:
            raise forms.ValidationError('A data inicial e final tem que estar definida!')

        cal = Brazil()
        data_dia_util_fim = cal.add_working_days(cleaned_data['data_inicial'] , 5)
        
        #delta = cleaned_data['data_final'] - cleaned_data['data_inicial'] 
        if data_dia_util_fim < cleaned_data['data_final']:
            self._errors['data_inicial'] = self.error_class(
                ['O período entre data inicial e final tem que ser de no máximo 5 dias úteis!']
                )

            self._errors['data_inicial'] = self.error_class(
                ['O período entre data inicial e final tem que ser de no máximo 5 dias úteis!']
                )
            raise forms.ValidationError(
                'O período entre data inicial e final tem que ser de no máximo 5 dias úteis!'
                )

        if cleaned_data['data_inicial'] >  cleaned_data['data_final']:
            self._errors['data_inicial'] = self.error_class(
                ['A data inicial não pode ser maior que a data final!']
                )

            self._errors['data_inicial'] = self.error_class(
                ['A data inicial não pode ser maior que a data final!']
                )
            raise forms.ValidationError('A data inicial não pode ser maior que a data final!')

        return cleaned_data


    class Meta:
        model = Cotacao
        fields = '__all__'