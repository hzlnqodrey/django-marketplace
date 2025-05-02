from django import forms

from .models import Item

INPUT_STYLE_CLASS = 'w-full py-4 px-6 rounded-xl border'

class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price', 'image',)

        widgets = {
            'category': forms.Select(attrs= {
                'class': INPUT_STYLE_CLASS,
            }),
            'name': forms.TextInput(attrs= {
                'class': INPUT_STYLE_CLASS,
            }),
            'description': forms.Textarea(attrs= {
                'class': INPUT_STYLE_CLASS,
            }),
            'price': forms.TextInput(attrs= {
                'class': INPUT_STYLE_CLASS,
            }),
            'image': forms.FileInput(attrs= {
                'class': INPUT_STYLE_CLASS,
            }),
        }

class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'description', 'price', 'image', 'is_sold')

        widgets = {
            'name': forms.TextInput(attrs= {
                'class': INPUT_STYLE_CLASS,
            }),
            'description': forms.Textarea(attrs= {
                'class': INPUT_STYLE_CLASS,
            }),
            'price': forms.TextInput(attrs= {
                'class': INPUT_STYLE_CLASS,
            }),
            'image': forms.FileInput(attrs= {
                'class': INPUT_STYLE_CLASS,
            }),
        }