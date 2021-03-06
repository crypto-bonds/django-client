from django.db.models import Q
from django.shortcuts import render
from datetime import datetime
from .models import Bank, Trader, Company, Bond

def index(request):
    return render(request, 'cryptoserver/index.html')


def signin(request):
    username = request.POST['InputName']
    password = request.POST['InputPassword']
    selection = request.POST['inlineFormCustomSelect']

    if selection == '1':
        try:
            if Bank.objects.filter(Q(username=username) & Q(password=password)).exists():
                bank = Bank.objects.get(Q(username=username) & Q(password=password))
                return render(request, 'cryptoserver/bank_main.html', {'bank': bank})
            else:
                return render(request, 'cryptoserver/index.html', {'message': 'Invalid username or password'})
        except Exception as e:
            print(e)
            return render(request, 'cryptoserver/Error_404.html')

    elif selection == '2':
        try:

            if Company.objects.filter(Q(username=username) & Q(password=password)).exists():
                company = Company.objects.get(Q(username=username) & Q(password=password))
                return render(request, 'cryptoserver/company_main.html',  {'company': company})
            else:
                return render(request, 'cryptoserver/index.html', {'message': 'Invalid username or password'})
        except:
            return render(request, 'cryptoserver/Error_404.html')
    else:
        try:
            if Trader.objects.filter(Q(username=username) & Q(password=password)).exists():
                trader = Trader.objects.get(Q(username=username) & Q(password=password))
                bonds = Bond.objects.all()
                return render(request, 'cryptoserver/trader_main.html', {'trader': trader, 'bonds': bonds})
            else:
                return render(request, 'cryptoserver/index.html', {'message': 'Invalid username or password'})
        except:
            return render(request, 'cryptoserver/Error_404.html')

def cwithdraw(request, company_id):
    company = Company.objects.get(pk=company_id)
    return render(request, 'cryptoserver/company_withdraw.html', {'company': company})

def cdeposit(request, company_id):
    company = Company.objects.get(pk=company_id)
    return render(request, 'cryptoserver/company_deposit.html', {'company': company})

def crequest(request, company_id):
    company = Company.objects.get(pk=company_id)
    return render(request, 'cryptoserver/company_request.html', {'company': company})

def bond_request(request):
    bank = Bank.objects.get(name=request.POST['bank_name'])
    company = Company.objects.get(id=request.POST['company_id'])
    try:
        Bond(issuer=company, underwriter=bank, amount=int(request.POST['amount']), denomination=int(request.POST['denomination']),
            interest_rate=int(request.POST['interest_rate']), maturity_date=datetime.strptime(request.POST['maturity_date'], '%m/%d/%Y')).save()
        return render(request, 'cryptoserver/company_main.html', {'company': company, 'message': 'Bond has been requested!'})
    except:
        return render(request, 'cryptoserver/company_main.html', {'company': company, 'message': 'There was an error in requesting bond... Try again later'})

def bdeposit(request, bank_id):
    bank = Bank.objects.get(pk=bank_id)
    return render(request, 'cryptoserver/bank_deposit.html', {'bank': bank})

def bwithdraw(request, bank_id):
    bank = Bank.objects.get(pk=bank_id)
    return render(request, 'cryptoserver/bank_withdraw.html', {'bank': bank})

def baccept(request, bank_id):
    bank = Bank.objects.get(pk=bank_id)
    return render(request, 'cryptoserver/bank_accept.html', {'bank': bank})

def bclear(request):
    try:
        bond = Bond.objects.get(id=request.POST['bond_id'])
        bank = Bank.objects.get(id=bond.underwriter.id)
        bond.cleared = True
        bond.save()
        return render(request, 'cryptoserver/bank_main.html', {'bank': bank, 'message': 'Bond has been accepted and entered into the system'})
    except:
        return render(request, 'cryptoserver/bank_main.html',
                      {'bank': bank, 'message': "Couldn't issue the bond... Try again later!"})


def tdeposit(request, trader_id):
    trader = Trader.objects.get(id=trader_id)
    return render(request, 'cryptoserver/trader_deposit.html', {'trader': trader})

def twithdraw(request, trader_id):
    trader = Trader.objects.get(id=trader_id)
    return render(request, 'cryptoserver/trader_withdraw.html', {'trader': trader})

def tbuy(request, trader_id):
    trader = Trader.objects.get(id=trader_id)
    bonds = Bond.objects.all()
    return render(request, 'cryptoserver/trader_buy.html', {'trader': trader, 'bonds': bonds})

def ttrade(request, trader_id):
    trader = Trader.objects.get(id=trader_id)
    return render(request, 'cryptoserver/trader_buy.html', {'trader': trader})

def buy_bond(request):
    try:
        trader = Trader.objects.get(id=request.POST['trader_id'])
        bond = Bond.objects.get(id=request.POST['bond_id'])
        bond.owner = trader
        bond.save()
        return render(request, 'cryptoserver/trader_main.html', {'trader': trader, 'message': 'Congragulation! You have succesfully acquired the bond worth $' + str(bond.amount)})
    except:
        return render(request, 'cryptoserver/trader_main.html', {'trader': trader,
                                                                 'message': 'Error occured in processing bond... please try later'})

def logout(request):
    return index(request)
