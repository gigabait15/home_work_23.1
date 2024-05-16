from django import forms

from catalog.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    def clean_name(self):
        clean_data = self.cleaned_data['name']
        ban_list = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

        for item_ban in ban_list:
            if item_ban in clean_data:
                raise forms.ValidationError(f'{item_ban} запрещенное слово')

        return clean_data

    def clean_description(self):
        clean_data = self.cleaned_data['description']
        ban_list = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

        for item_ban in ban_list:
            if item_ban in clean_data:
                raise forms.ValidationError(f'{item_ban} запрещенное слово')

        return clean_data


class VersionForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Version
        fields = ('name', 'number_version', 'current_version_indicator')



