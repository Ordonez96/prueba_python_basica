from django.shortcuts import render, redirect, get_object_or_404
from .models import Account, Transaction
from decimal import Decimal

def home(request):
    # Obtener todas las cuentas
    accounts = Account.objects.all()
    return render(request, 'bank/home.html', {'accounts': accounts})

def add_transaction(request):
    if request.method == 'POST':
        # Obtener el account_id desde el formulario
        account_id = request.POST.get('account_id')  
        
        # Obtener la cuenta correspondiente
        account = get_object_or_404(Account, id=account_id)
        
        # Obtener el tipo de transacción y la cantidad
        transaction_type = request.POST['transaction_type']
        amount = Decimal(request.POST['amount'])

        # Verificar si es una retirada y si hay suficientes fondos
        if transaction_type == 'withdrawal' and account.balance < amount:
            return render(request, 'bank/alert.html', {'message': 'Insufficient funds to complete the transaction'})

        # Realizar la transacción
        if transaction_type == 'deposit':
            account.balance += amount
        elif transaction_type == 'withdrawal':
            account.balance -= amount

        account.save()

        # Crear la transacción asociada a la cuenta
        Transaction.objects.create(account=account, transaction_type=transaction_type, amount=amount)
        
        # Redirigir a la página de transacciones de la cuenta
        return redirect('account_transactions', account_id=account.id)

    # Si el método no es POST, obtener la cuenta con el ID pasado como parámetro
    account_id = request.GET.get('account_id')
    account = get_object_or_404(Account, id=account_id)

    return render(request, 'bank/add_transaction.html', {'account': account})


def create_account(request):
    if request.method == 'POST':
        # Crear una nueva cuenta con saldo inicial 0
        Account.objects.create(balance=Decimal('0.00'))
        return redirect('home')  # Redirigir a la página de inicio

    return render(request, 'bank/create_account.html')

def delete_account(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    account.delete()
    return redirect('home')  # Redirigir a la página de inicio

def account_transactions(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    transactions = Transaction.objects.filter(account=account).order_by('-created_at')
    return render(request, 'bank/account_transactions.html', {'account': account, 'transactions': transactions})
