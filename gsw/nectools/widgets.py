from django.forms import widgets


class DateInput(widgets.TextInput):
    input_type = 'date'
