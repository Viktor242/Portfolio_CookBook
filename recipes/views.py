from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from recipes.forms import RecipeForm, CommentForm, RatingForm
from recipes.models import Recipe, Rating


def index(request):
    return HttpResponse("Раздел рецептов работает!")

class HomePageView(ListView):
    """Главная страница — приветствие и несколько рецептов"""
    model = Recipe
    template_name = "main/home.html"
    context_object_name = "recipes"

    def get_queryset(self):
        return Recipe.objects.order_by("-created_at")[:5]  # последние 5 рецептов


class RecipeCreateView(LoginRequiredMixin, CreateView):
    """Добавление рецепта"""
    model = Recipe
    form_class = RecipeForm
    template_name = "recipes/recipe_form.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


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


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование рецепта"""
    model = Recipe
    form_class = RecipeForm
    template_name = "recipes/recipe_edit.html"

    def get_success_url(self):
        return reverse_lazy("my_recipes")

    def test_func(self):
        """Разрешаем редактировать только автору рецепта"""
        recipe = self.get_object()
        return recipe.author == self.request.user