# from django import forms
# from .models import City

# def get_city_choice():
#     choice = []
#     for city in City.objects.all():
#         choice.append((city.shortcut, city.name))
#     return choice

# class FilterForm(forms.Form):
#     priceMin = forms.IntegerField(label='Cena minimalna', required=False, min_value=0, initial=0)
#     priceMax = forms.IntegerField(label='Cena maksymalna', required=False, min_value=0, initial=0)

#     cityWro = forms.BooleanField(label='Wocław', initial=True, required=False)
#     cityGda = forms.BooleanField(label='Gdansk', initial=True, required=False)
#     cityRze = forms.BooleanField(label='Rzeszów', initial=True, required=False)

#     priceMin.widget.attrs.update({'class':'form-control'})
#     priceMax.widget.attrs.update({'class':'form-control'})

#     cityWro.widget.attrs.update({'class':'form-check-input', 'value': 'WRO'})
#     cityGda.widget.attrs.update({'class':'form-check-input', 'value': 'GDA'})
#     cityRze.widget.attrs.update({'class':'form-check-input', 'value': 'RZE'})
