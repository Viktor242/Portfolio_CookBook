from django import forms
from django.forms import inlineformset_factory
from django.utils.html import format_html
from django.urls import reverse

from recipes.models import Recipe, Rating, Comment, RecipeIngredient, RecipeImage


class ImageFileInput(forms.FileInput):
    """Кастомный виджет для отображения существующих изображений"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        
        # Если есть существующее изображение, показываем его название
        if value and hasattr(value, 'name'):
            current_file = f"""
            <div class="current-image-info" style="margin-top: 5px; padding: 8px; background: #e9ecef; border-radius: 4px; font-size: 14px;">
                <strong>Текущее изображение:</strong> {value.name}
                <br><small class="text-muted">Выберите новое изображение для замены</small>
            </div>
            """
            html += current_file
        
        return format_html(html)


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
    extra=0,
    can_delete=True
)

# Formset для создания нового рецепта (с одним пустым полем)
RecipeIngredientFormSetCreate = inlineformset_factory(
    Recipe,
    RecipeIngredient,
    form=RecipeIngredientForm,
    extra=1,
    can_delete=True
)

# Formset для редактирования существующего рецепта (без пустого поля по умолчанию)
RecipeImageFormSet = inlineformset_factory(
    Recipe,
    RecipeImage,
    fields=("image",),
    extra=0,
    can_delete=True,
    widgets={
        'image': ImageFileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        })
    }
)

# Formset для создания нового рецепта (с одним пустым полем)
RecipeImageFormSetCreate = inlineformset_factory(
    Recipe,
    RecipeImage,
    fields=("image",),
    extra=1,
    can_delete=True,
    widgets={
        'image': forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
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
        widgets = {
            'value': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5,
                'step': 1,
                'placeholder': 'Оценка от 1 до 5',
                'required': True
            })
        }