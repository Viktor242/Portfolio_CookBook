from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from recipes.models import Recipe, Category
from .models import Collection, CollectionItem
from .forms import CollectionForm


@login_required
def collection_list(request):
    my_collections = request.user.collections.all()
    public_collections = Collection.objects.filter(is_public=True)
    categories = Category.objects.all()

    return render(
        request,
        "collections/collection_list.html",
        {
            "my_collections": my_collections,
            "public_collections": public_collections,
            "categories": categories,
        },
    )

@login_required
def collection_create(request):
    if request.method == "POST":
        form = CollectionForm(request.POST)
        if form.is_valid():
            collection = form.save(commit=False)
            collection.owner = request.user
            collection.save()
            return redirect("collection_list")
    else:
        form = CollectionForm()
    return render(request, "collections/collection_form.html", {
        "form": form,
        "editing": False,
    })

@login_required
def collection_edit(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    if collection.owner != request.user:
        return HttpResponseForbidden("Нет доступа")

    if request.method == "POST":
        form = CollectionForm(request.POST, instance=collection)
        if form.is_valid():
            form.save()
            return redirect("collection_list")
    else:
        form = CollectionForm(instance=collection)

    return render(request, "collections/collection_form.html", {
        "form": form,
        "editing": True,
    })


@login_required
def collection_delete(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    if collection.owner != request.user:
        return HttpResponseForbidden("Нет доступа")

    if request.method == "POST":
        collection.delete()
        return redirect("collection_list")

    return render(request, "collections/collection_confirm_delete.html", {
        "collection": collection,
    })


@login_required
def collection_detail(request, pk):
    collection = get_object_or_404(Collection, pk=pk)

    # доступ:
    if collection.owner != request.user and not collection.is_public:
        return HttpResponseForbidden("Эта коллекция приватная")

    return render(request, "collections/collection_detail.html", {"collection": collection})


@login_required
def toggle_recipe_in_collection(request, recipe_id, collection_id):
    """Добавить/удалить рецепт в коллекции"""
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    collection = get_object_or_404(Collection, pk=collection_id, owner=request.user)

    item, created = CollectionItem.objects.get_or_create(collection=collection, recipe=recipe)
    if not created:
        item.delete()
        in_collection = False
    else:
        in_collection = True

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"in_collection": in_collection})

    # Перенаправляем на страницу коллекции, а не рецепта
    return redirect("collection_detail", pk=collection_id)


@login_required
@require_http_methods(["GET"])
def api_user_collections(request):
    """API endpoint для получения коллекций пользователя"""
    try:
        collections = request.user.collections.all()
        collections_data = []
        
        for collection in collections:
            collections_data.append({
                'id': collection.id,
                'title': collection.title,
                'description': collection.description,
                'is_public': collection.is_public,
                'items_count': collection.items.count()
            })
        
        return JsonResponse({
            'success': True,
            'collections': collections_data
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def api_add_recipe_to_collection(request):
    """API endpoint для добавления рецепта в коллекцию"""
    try:
        data = json.loads(request.body)
        collection_id = data.get('collection_id')
        recipe_id = data.get('recipe_id')
        
        if not collection_id or not recipe_id:
            return JsonResponse({
                'success': False,
                'error': 'Не указаны ID коллекции или рецепта'
            })
        
        # Проверяем, что коллекция принадлежит пользователю
        collection = get_object_or_404(Collection, pk=collection_id, owner=request.user)
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        
        # Добавляем рецепт в коллекцию
        item, created = CollectionItem.objects.get_or_create(
            collection=collection, 
            recipe=recipe
        )
        
        if created:
            return JsonResponse({
                'success': True,
                'message': f'Рецепт "{recipe.title}" добавлен в коллекцию "{collection.title}"'
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Рецепт уже находится в этой коллекции'
            })
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Неверный формат JSON'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def api_remove_recipe_from_collection(request):
    """API endpoint для удаления рецепта из коллекции"""
    try:
        data = json.loads(request.body)
        collection_id = data.get('collection_id')
        recipe_id = data.get('recipe_id')
        
        if not collection_id or not recipe_id:
            return JsonResponse({
                'success': False,
                'error': 'Не указаны ID коллекции или рецепта'
            })
        
        # Проверяем, что коллекция принадлежит пользователю
        collection = get_object_or_404(Collection, pk=collection_id, owner=request.user)
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        
        # Удаляем рецепт из коллекции
        try:
            item = CollectionItem.objects.get(collection=collection, recipe=recipe)
            item.delete()
            return JsonResponse({
                'success': True,
                'message': f'Рецепт "{recipe.title}" удален из коллекции "{collection.title}"'
            })
        except CollectionItem.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Рецепт не найден в этой коллекции'
            })
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Неверный формат JSON'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })