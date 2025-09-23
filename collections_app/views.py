from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from recipes.models import Recipe
from .models import Collection, CollectionItem
from .forms import CollectionForm


@login_required
def collection_list(request):
    my_collections = request.user.collections.all()
    public_collections = Collection.objects.filter(is_public=True).exclude(owner=request.user)

    return render(
        request,
        "collections/collection_list.html",
        {
            "my_collections": my_collections,
            "public_collections": public_collections,
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
    return render(request, "collections/collection_form.html", {"form": form})

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

    return redirect("recipe_detail", pk=recipe_id)