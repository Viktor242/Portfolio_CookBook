from django import forms
from django.forms import inlineformset_factory

from recipes.models import Recipe, Rating, Comment, RecipeIngredient, RecipeImage


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", "description", "instruction", "cook_time", "category", "difficulty"]

class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ["ingredient", "amount", "unit"]

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
    can_delete=True
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