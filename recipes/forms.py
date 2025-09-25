from django import forms
from django.forms import inlineformset_factory

from recipes.models import Recipe, Rating, Comment, RecipeIngredient, RecipeImage


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", "description", "instruction", "cook_time", "category", "difficulty"]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название рецепта',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Краткое описание блюда...',
                'rows': 3
            }),
            'instruction': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Пошаговая инструкция приготовления...',
                'rows': 6,
                'required': True
            }),
            'cook_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'required': True
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'difficulty': forms.Select(attrs={
                'class': 'form-control'
            })
        }

class RecipeIngredientForm(forms.ModelForm):
    UNIT_CHOICES = [
        ('', 'Ед. изм.'),
        ('шт', 'шт'),
        ('мл', 'мл'),
        ('г', 'г'),
        ('кг', 'кг'),
        ('л', 'л'),
        ('ст.л.', 'ст.л.'),
        ('ч.л.', 'ч.л.'),
        ('стакан', 'стакан'),
        ('щепотка', 'щепотка'),
    ]
    
    unit = forms.ChoiceField(
        choices=UNIT_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = RecipeIngredient
        fields = ["ingredient", "amount", "unit"]
        widgets = {
            'ingredient': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Количество',
                'required': True
            })
        }

RecipeIngredientFormSet = inlineformset_factory(
    Recipe,
    RecipeIngredient,
    form=RecipeIngredientForm,
    extra=1,
    can_delete=True
)

RecipeImageFormSet = inlineformset_factory(
    Recipe,
    RecipeImage,
    fields=("image", "is_main"),
    extra=1,
    can_delete=True,
    widgets={
        'image': forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        'is_main': forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    }
)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 3, "placeholder": "Ваш комментарий..."})
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["value"]