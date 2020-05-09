from django import forms
from tempus_dominus.widgets import DatePicker, TimePicker
from consulta.models import Consulta
from medico.views import listar_medico
from paciente.views import listar_paciente

class CadConsulta(forms.ModelForm):
	medico = forms.ChoiceField(label='Médicos disponíveis: ',)
	paciente = forms.ChoiceField(label='Paciente: ',)
	cpf = forms.CharField(label='CPF: ')
	
	class Meta:
		model = Consulta
		fields = ['cpf', 'paciente', 'data', 'hora', 'medico']
		labels = {'data':'Data:', 'medico':'Médicos :', 'hora':'Horário:', 'paciente':'Paciente:'}
		widgets = {
			'data': DatePicker(
				options={
				'minDate': 'moment',
				'daysOfWeekDisabled':[0, 6],
				
				'ignoreReadonly': True,
				},
				attrs={
				'readonly':'readonly',
                'append': 'fa fa-calendar',
                'icon_toggle': True,
				'class' : 'dt_hr',
            	}),
			'hora': TimePicker(
				options={
					'format':'LT',
					'enabledHours':[9, 10, 11, 12, 13, 14, 15, 16, 17],
					'stepping': 30,
					'defaultDate': '1970-01-01T14:56',
					'ignoreReadonly': True,
					
					},
				attrs={
					'readonly':'readonly',
					'input_toggle': True,
					'input_group': True,
					'append': 'far fa-clock',
					'class' : 'dt_hr',
				},),				
		}
