from django import forms

from recipes.models import Recipe, Rating, Comment


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", "description", "instruction", "cook_time", "category", "difficulty"]

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