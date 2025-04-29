from django.shortcuts import render
# import login decorator
from django.contrib.auth.decorators import login_required

# Importing Items to make a dashboard table

from item.models import Item


# Main Index
@login_required
def index(request):
    items = Item.objects.filter(created_by=request.user)

    return render(request, 'dashboard/index.html', {
        'items': items,
    })