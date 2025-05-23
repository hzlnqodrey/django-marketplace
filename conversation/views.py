from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from item.models import Item
from .models import Conversation
from .forms import ConversationMessageForm

# Create your views here.
@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    # Check if you are the owner
    # then u should not be able to visit this page, redirect user's owner
    if item.created_by == request.user:
        return redirect('dashboard:index')

    # Conversation Logic
    # Checking and Filter if the requested user id is matched with item object filter to conversation object
    # Make a new conversations
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    # If there is already conversation between Owner and Buyer
    if conversations:
        # redirected to conversation
        return redirect('conversation:detail', pk=conversations.first().id)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():

            # register every valid users
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            # craete the converstaion message
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            # redirect back to item
            return redirect('item:detail', pk=item_pk)
        
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/new.html', {
        'form': form
    })

# Get All of the Inbox requested
@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    return render(request, 'conversation/inbox.html', {
        'conversations': conversations
    })


# Get all the convos in inbox id of one of the item id 
@login_required
def detail(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

    # See if the form has been submitted
    # if yes, create a new conversation message
    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect('conversation:detail', pk=pk)
    
    # If there is no, craete empty convos form
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form
    })
