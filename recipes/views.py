from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from recipes.forms import RecipeForm, CommentForm, RatingForm, RecipeIngredientFormSet
from recipes.models import Recipe, Rating, Ingredient

PREFIX = "ingredients"

def index(request):
    return HttpResponse("Раздел рецептов работает!")

class HomePageView(ListView):
    """Главная страница — приветствие и несколько рецептов"""
    model = Recipe
    template_name = "main/home.html"
    context_object_name = "recipes"

    def get_queryset(self):
        return Recipe.objects.order_by("-created_at")[:5]  # последние 5 рецептов


@login_required
def recipe_create(request):
    prefix = "ingredients"
    if request.method == "POST":
        form = RecipeForm(request.POST)
        # сначала проверяем основную форму, чтобы сохранить объект и привязать formset к instance
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            formset = RecipeIngredientFormSet(request.POST, instance=recipe, prefix=prefix)
            if formset.is_valid():
                formset.save()
                return redirect("recipe_detail", pk=recipe.pk)
        else:
            # если основная форма невалидна — всё равно прикрепляем formset из POST,
            # чтобы показать ошибки полей ингредиентов
            formset = RecipeIngredientFormSet(request.POST, prefix=prefix)
    else:
        form = RecipeForm()
        # создаём «пустой» instance, чтобы у formset корректно работал empty_form и prefix
        recipe = Recipe()
        formset = RecipeIngredientFormSet(instance=recipe, prefix=prefix)

    return render(request, "recipes/recipe_form.html", {"form": form, "formset": formset})


@login_required
def recipe_edit(request, pk):
    """
    Редактирование: валидируем одновременно main form и formset; при успехе — сохраняем.
    """
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.author != request.user:
        return HttpResponseForbidden("Нет доступа")

    if request.method == "POST":
        form = RecipeForm(request.POST, instance=recipe)
        formset = RecipeIngredientFormSet(request.POST, instance=recipe, prefix=PREFIX)

        if form.is_valid() and formset.is_valid():
            # Сохраняем main form и formset
            recipe = form.save()
            formset.instance = recipe
            formset.save()
            return redirect("my_recipes")
        else:
            # Debug: вывести ошибки в серверный лог (временно)
            print("Recipe edit: form valid?", form.is_valid(), "form errors:", form.errors)
            print("Recipe edit: formset valid?", formset.is_valid(), "formset non_field:", formset.non_form_errors(), "forms errors:", [f.errors for f in formset.forms])
    else:
        form = RecipeForm(instance=recipe)
        formset = RecipeIngredientFormSet(instance=recipe, prefix=PREFIX)

    return render(request, "recipes/recipe_form.html", {"form": form, "formset": formset, "editing": True})

@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.author != request.user:
        return HttpResponseForbidden("Нет доступа")

    if request.method == "POST":
        recipe.delete()
        return redirect("my_recipes")

    return render(request, "recipes/recipe_confirm_delete.html", {
        "recipe": recipe,
    })

class RecipeDetailView(DetailView):
    """Страница рецепта с комментариями и оценками"""
    model = Recipe
    template_name = "recipes/recipe_detail.html"
    context_object_name = "recipe"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        context["rating_form"] = RatingForm()
        context["comments"] = self.object.comments.all()
        if self.request.user.is_authenticated:
            collections = self.request.user.collections.all()
            recipe = self.get_object()
            context["collections"] = [
                {"obj": c, "in_collection": c.items.filter(recipe=recipe).exists()}
                for c in collections
            ]
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if "text" in request.POST:  # комментарий
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.recipe = self.object
                comment.user = request.user
                comment.save()
                return redirect("recipe_detail", pk=self.object.pk)

        if "value" in request.POST:  # оценка
            form = RatingForm(request.POST)
            if form.is_valid():
                Rating.objects.update_or_create(
                    recipe=self.object,
                    user=request.user,
                    defaults={"value": form.cleaned_data["value"]},
                )
                return redirect("recipe_detail", pk=self.object.pk)

        return self.get(request, *args, **kwargs)

class RecipeListView(ListView):
    """Список всех рецептов"""
    model = Recipe
    template_name = "recipes/recipe_list.html"
    context_object_name = "recipes"
    paginate_by = 10  # по 10 рецептов на страницу

    def get_queryset(self):
        return Recipe.objects.order_by("-created_at")

class MyRecipesView(LoginRequiredMixin, ListView):
    """Список рецептов текущего пользователя"""
    model = Recipe
    template_name = "recipes/my_recipes.html"
    context_object_name = "recipes"
    paginate_by = 10

    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user).order_by("-created_at")


class IngredientListView(LoginRequiredMixin, ListView):
    """Список всех ингредиентов"""
    model = Ingredient
    template_name = "recipes/ingredient_list.html"
    context_object_name = "ingredients"
    paginate_by = 20

    def get_queryset(self):
        return Ingredient.objects.order_by("name")


class IngredientCreateView(LoginRequiredMixin, CreateView):
    """Добавление нового ингредиента"""
    model = Ingredient
    template_name = "recipes/ingredient_form.html"
    fields = ["name", "default_unit"]
    success_url = reverse_lazy("ingredient_list")