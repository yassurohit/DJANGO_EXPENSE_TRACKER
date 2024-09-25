from django.contrib import messages
from django.shortcuts import render,redirect
from tracker.models import TrackingHistory,CurrentBalance

# Create your views here.

def index(request):
    if request.method == "POST":
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        expense_type = "CREDIT"
        
        if not amount:
            messages.error(request, "Amount field cannot be empty")
            return redirect('/')
        
        if float(amount) < 0:
            expense_type = "DEBIT"
        
        if float(amount) == 0:
            messages.error(request, "Amount cannot be zero")
            return redirect('/')
        
        current_balance, created = CurrentBalance.objects.get_or_create(id=1)
        tracking_history = TrackingHistory.objects.create(amount=amount, description=description, expense_type=expense_type, current_balance=current_balance)
        current_balance.current_balance += float(tracking_history.amount)
        current_balance.save()
        
        messages.success(request, "Transaction recorded successfully!")
        return redirect('/')
    
    current_balance, created = CurrentBalance.objects.get_or_create(id=1)
    income = 0
    expense = 0
    for trans in TrackingHistory.objects.all():
        if trans.expense_type == 'CREDIT':
            income += trans.amount
        else:
            expense += trans.amount
    
    context = {
        'transactions': TrackingHistory.objects.all(),
        'current_balance': current_balance,
        'income': income,
        'expense': expense
    }
    return render(request, 'index.html', context)

def delete_transaction(request,id):
    transaction = TrackingHistory.objects.filter(id=id)
    if transaction.exists:
        current_balance,created=CurrentBalance.objects.get_or_create(id=1)
        print(transaction)
        tracking_history = transaction[0]
        current_balance.current_balance -= tracking_history.amount
        current_balance.save()
        transaction.delete()
    return redirect('/')