from django import forms
from tempus_dominus.widgets import DatePicker, TimePicker
from datetime import datetime



class cadConsulta(forms.Form):
	medico = forms.ChoiceField(label='Médico')
	convenio = forms.ChoiceField(label='Convênio')
	data = forms.DateField(label='Data', widget=DatePicker(
		options={
			'minDate': 'moment',
            }
			))
	hora = forms.TimeField(label='Hora', widget=TimePicker(
		options={
			'format':'LT',
            'enabledHours':[9, 10, 11, 12, 13, 14, 15, 16, 17],
		    'stepping': 30,
            'defaultDate': '1970-01-01T14:56',
			}
		))
	