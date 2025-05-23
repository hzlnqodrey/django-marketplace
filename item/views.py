from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from item.models import Item, Category
from .forms import NewItemForm, EditItemForm


# List View
def items_browse(request):
    query = request.GET.get('query', '')

    categories = Category.objects.all()
    category_id = request.GET.get('category', 0)

    items = Item.objects.filter(is_sold=False)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description_icontains=query))

    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id)
    })


# Detail View.
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)

    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items
    })

# CRUD
# Add Decorator for: add new item if user is logged in
# if not authenticated, the user/guess will be redirected to login page
@login_required
def new(request):

    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            # commit false because "createdBy" field still not there, therefore it will cause error in DB
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            # redirect user to the detailed new item page
            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New Item'
    })

@login_required
def delete(request, pk):
    items = get_object_or_404(Item, pk=pk, created_by=request.user)
    items.delete()

    return redirect('dashboard:index')

@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            # redirect user to the detailed new item page
            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit Item'
    })
