from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from item.models import Item
from .forms import NewItemForm

# Create your views here.
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)

    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items
    })


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