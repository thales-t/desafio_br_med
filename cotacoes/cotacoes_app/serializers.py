from rest_framework import serializers
from cotacoes_app.models import CotacaoApi
from rest_framework.validators import UniqueTogetherValidator
from workalendar.america import Brazil


class DiaUtilValidator:
    message = ('Só deve ser registrado dia útil! O(s) campo(s)  {erro_fields} não são ')

    def __init__(self, fields, message=None):
        self.fields = fields
        self.message = message or self.message

    def __call__(self, value):
        cal = Brazil()
        erro_fields = []
        for field in self.fields:
            if not cal.is_working_day(value[field]):
                erro_fields.append(f'{field}:{value[field]}')
        if erro_fields:        
            message = self.message.format(erro_fields=erro_fields)
            raise serializers.ValidationError(message, code='work_day')


class CotacaoApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = CotacaoApi
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=CotacaoApi.objects.all(),
                fields=['data', 'moeda_cotada'],
                message='Não pode ter duas cotacões para a mesma moeda no mesmo dia!'
            ),
            DiaUtilValidator(
                fields=['data'],
            )
        ]


            