from django.shortcuts import render
from .models import *
from .forms import StockSearchForm
from json import dumps
import json
import datetime
from membership.models import Customer
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from ast import literal_eval

# Create your views here.
@login_required
def list_items(request):
    title = 'List of Items'
    form = StockSearchForm(request.POST or None)
    queryset = Inventory.objects.all()
    context = {
        "form": form,
        'title': title,
        'queryset': queryset,
        "head": "TRANSACTION",

    }
    if request.method == 'POST':
        queryset = Inventory.objects.filter(category__icontains=form['category'].value(),
                                            item_code__icontains=form['item_code'].value(),
                                            item_name__icontains=form['item_name'].value())
        context = {
            "form": form,
            "header": title,
            "queryset": queryset,
            "head": "TRANSACTION",
        }
    return render(request, 'system/inventory_view.html', context)

@login_required
def transaction(request):
    title = 'List of Items'
    queryset = Inventory.objects.all()
    form = StockSearchForm(request.POST or None)

    context = {
        "form": form,
        'title': title,
        'queryset': queryset,
        "head": "TRANSACTION",
    }
    # search inventory items
    if request.method == 'POST':
        queryset = Inventory.objects.filter(category__icontains=form['category'].value(),
                                            item_code__icontains=form['item_code'].value(),
                                            item_name__icontains=form['item_name'].value())
        purchaseDetails = request.POST.get('purchaseDetails2')
        dataJSON = dumps(purchaseDetails)
        print(purchaseDetails)
        context = {
            "form": form,
            "header": title,
            "queryset": queryset,
            "salesValues": dataJSON,
            "head": "TRANSACTION",
        }
    return render(request, 'system/reciept_form.html', context)


@login_required
def submitDetails(request):
    #  when clicked proceed
    purchaseDetails = request.POST.get('purchaseDetails')
    total = request.POST.get('totalValue')
    print(purchaseDetails)
    dataJSON = dumps(purchaseDetails)
    print(dataJSON)
    context = {
        "date": datetime.datetime.now(),
        "purchaseItems": dataJSON,
        "purchaseDetails": purchaseDetails,
        "total": total,
        "head": "TRANSACTION",
    }
    return render(request, 'system/submitDetails.html', context)


def savePurchaseDetails(request):
    if request.method == 'POST':
    # store purchase details
        customerPhone = request.POST.get('phone')
        discountt = int(float(request.POST.get('offer', 0)))
        newTotal = request.POST.get('newVal', 0)
        try:
            customer_fk = Customer.objects.get(phone=customerPhone)
            purchase = Sales(total_price=int(float(newTotal)), customer=customer_fk, discount=discountt, created_by=request.user)
        except:
            purchase = Sales(total_price=int(float(newTotal)), discount=discountt, created_by=request.user)
            #handle no customer with phone here
        purchase.save()
        purchaseDetails = literal_eval(request.POST.get('purchaseDetails')) #converting html data into python datatype
        sales_fk = Sales.objects.last()#get the last record of Sales
        print(sales_fk)
        print(type(purchaseDetails))
    #store Item purchased details
        for item in purchaseDetails:
            item_id = item['ID'].strip()
            item_ids = Inventory.objects.get(item_code=item_id)
            quantity = int(item['quantity'])
            line_total = int(item['line total'])
            print(item_id,quantity, line_total)
            purchaseItem = SalesItem(sales=sales_fk, item=item_ids, purchase_unit=quantity, line_total=line_total)
            purchaseItem.save()
        #update in_stock of the items purchased
            item_ids.in_stock = item_ids.in_stock - int(item['quantity'])
            item_ids.save()
    return render(request, 'system/success.html')
