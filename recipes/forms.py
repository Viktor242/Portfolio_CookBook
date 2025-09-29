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


# Создаем базовый formset
RecipeIngredientFormSetBase = inlineformset_factory(
    Recipe,
    RecipeIngredient,
    form=RecipeIngredientForm,
    extra=0,
    can_delete=True
)

# Кастомный formset для обработки дубликатов ингредиентов
class RecipeIngredientFormSet(RecipeIngredientFormSetBase):
    def clean(self):
        """Кастомная валидация для обработки пустых форм и дубликатов"""
        # Сначала обрабатываем пустые формы
        for form in self.forms:
            if form.cleaned_data:
                # Если форма пустая (нет ингредиента или количества), помечаем для удаления
                if not form.cleaned_data.get('ingredient') or not form.cleaned_data.get('amount'):
                    form.cleaned_data['DELETE'] = True
                    # Очищаем ошибки для пустых форм
                    form._errors = {}
            else:
                # Если cleaned_data пустой, создаем пустой словарь с DELETE=True
                form.cleaned_data = {'DELETE': True}
                form._errors = {}
        
        # Вызываем стандартную валидацию
        cleaned_data = super().clean()
        
        # Проверяем дубликаты ингредиентов
        ingredients = []
        deleted_ingredient_ids = []
        duplicate_ingredients = []
        
        for form in self.forms:
            if (form.cleaned_data and 
                form.cleaned_data.get('ingredient') and 
                form.cleaned_data.get('amount') and
                not form.cleaned_data.get('DELETE')):
                # Добавляем ингредиент в список для проверки дубликатов
                ingredient = form.cleaned_data.get('ingredient')
                ingredient_id = ingredient.pk
                ingredient_name = ingredient.name
                
                if ingredient_id in ingredients:
                    duplicate_ingredients.append(ingredient_name)
                else:
                    ingredients.append(ingredient_id)
        
        # Если есть дубликаты, показываем предупреждение
        if duplicate_ingredients:
            duplicate_names = ', '.join(duplicate_ingredients)
            raise forms.ValidationError(
                f"⚠️ Внимание: Ингредиенты '{duplicate_names}' добавлены несколько раз. "
                f"Удалите дубликаты или выберите другие ингредиенты."
            )
        
        return cleaned_data
    
    

# Formset для создания нового рецепта (с одним пустым полем)
RecipeIngredientFormSetCreate = inlineformset_factory(
    Recipe,
    RecipeIngredient,
    form=RecipeIngredientForm,
    formset=RecipeIngredientFormSet,
    extra=1,
    can_delete=True
)

# Кастомный формсет для изображений с правильной обработкой удаления
class RecipeImageFormSetBase(inlineformset_factory(
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
)):
    def clean(self):
        """Кастомная валидация для обработки удаления изображений"""
        for form in self.forms:
            if form.cleaned_data and form.cleaned_data.get('DELETE', False):
                # Если изображение помечено для удаления, очищаем поле image
                form.cleaned_data['image'] = None
        return super().clean()
    
    def is_valid(self):
        """Переопределяем is_valid для правильной обработки пустых форм и удаления"""
        # Сначала вызываем стандартную валидацию
        valid = super().is_valid()
        
        if not valid:
            # Проверяем, есть ли ошибки только из-за пустых форм или удаления
            for form in self.forms:
                if hasattr(form, 'cleaned_data') and form.cleaned_data:
                    # Если форма пустая (нет изображения) или помечена для удаления, очищаем ошибки
                    if not form.cleaned_data.get('image') or form.cleaned_data.get('DELETE', False):
                        form._errors = {}
                elif not hasattr(form, 'cleaned_data') or not form.cleaned_data:
                    # Пустая форма - считаем валидной
                    form._errors = {}
            
            # Проверяем, остались ли ошибки после очистки пустых форм
            has_errors = any(form.errors for form in self.forms)
            return not has_errors
        
        return valid
    
    def save(self, commit=True):
        """Переопределяем save для правильного удаления изображений"""
        if not self.is_valid():
            return self.save_existing_objects(commit) and self.save_new_objects(commit)
        
        print(f"DEBUG: RecipeImageFormSet save() - commit={commit}")
        print(f"DEBUG: Количество форм: {len(self.forms)}")
        
        # Обрабатываем удаление изображений
        deleted_objects = []
        for i, form in enumerate(self.forms):
            print(f"DEBUG: Форма {i}: cleaned_data={form.cleaned_data}")
            if form.cleaned_data and form.cleaned_data.get('DELETE', False):
                if form.instance.pk:
                    print(f"DEBUG: Помечено для удаления: {form.instance.pk}")
                    deleted_objects.append(form.instance)
                else:
                    print(f"DEBUG: Форма помечена для удаления, но нет instance.pk")
        
        print(f"DEBUG: Объектов для удаления: {len(deleted_objects)}")
        
        # Удаляем помеченные объекты
        for obj in deleted_objects:
            print(f"DEBUG: Удаляем объект {obj.pk}")
            obj.delete()
        
        # Сохраняем остальные объекты
        result = super().save(commit)
        print(f"DEBUG: RecipeImageFormSet save() завершен")
        return result

# Formset для редактирования существующего рецепта (без пустого поля по умолчанию)
RecipeImageFormSet = RecipeImageFormSetBase

# Кастомный формсет для создания рецепта с правильной обработкой удаления
class RecipeImageFormSetCreateBase(inlineformset_factory(
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
)):
    def clean(self):
        """Кастомная валидация для обработки удаления изображений"""
        for form in self.forms:
            if form.cleaned_data and form.cleaned_data.get('DELETE', False):
                # Если изображение помечено для удаления, очищаем поле image
                form.cleaned_data['image'] = None
        return super().clean()
    
    def is_valid(self):
        """Переопределяем is_valid для правильной обработки пустых форм и удаления"""
        # Сначала вызываем стандартную валидацию
        valid = super().is_valid()
        
        if not valid:
            # Проверяем, есть ли ошибки только из-за пустых форм или удаления
            for form in self.forms:
                if hasattr(form, 'cleaned_data') and form.cleaned_data:
                    # Если форма пустая (нет изображения) или помечена для удаления, очищаем ошибки
                    if not form.cleaned_data.get('image') or form.cleaned_data.get('DELETE', False):
                        form._errors = {}
                elif not hasattr(form, 'cleaned_data') or not form.cleaned_data:
                    # Пустая форма - считаем валидной
                    form._errors = {}
            
            # Проверяем, остались ли ошибки после очистки пустых форм
            has_errors = any(form.errors for form in self.forms)
            return not has_errors
        
        return valid
    
    def save(self, commit=True):
        """Переопределяем save для правильного удаления изображений"""
        if not self.is_valid():
            return self.save_existing_objects(commit) and self.save_new_objects(commit)
        
        print(f"DEBUG: RecipeImageFormSet save() - commit={commit}")
        print(f"DEBUG: Количество форм: {len(self.forms)}")
        
        # Обрабатываем удаление изображений
        deleted_objects = []
        for i, form in enumerate(self.forms):
            print(f"DEBUG: Форма {i}: cleaned_data={form.cleaned_data}")
            if form.cleaned_data and form.cleaned_data.get('DELETE', False):
                if form.instance.pk:
                    print(f"DEBUG: Помечено для удаления: {form.instance.pk}")
                    deleted_objects.append(form.instance)
                else:
                    print(f"DEBUG: Форма помечена для удаления, но нет instance.pk")
        
        print(f"DEBUG: Объектов для удаления: {len(deleted_objects)}")
        
        # Удаляем помеченные объекты
        for obj in deleted_objects:
            print(f"DEBUG: Удаляем объект {obj.pk}")
            obj.delete()
        
        # Сохраняем остальные объекты
        result = super().save(commit)
        print(f"DEBUG: RecipeImageFormSet save() завершен")
        return result

# Formset для создания нового рецепта (с одним пустым полем)
RecipeImageFormSetCreate = RecipeImageFormSetCreateBase


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