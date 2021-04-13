from django.shortcuts import render
from .models import *
from .forms import StockSearchForm
from json import dumps
import datetime
from membership.models import Customer
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ast import literal_eval
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.http import HttpResponse
from SalesInventory.utils import render_to_pdf  #created in step 4



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
    return render(request, 'system/add_to_cart.html', context)

@login_required
def submitDetails(request):
    #  when clicked proceed
    purchaseDetails = request.POST.get('purchaseDetails')
    total = request.POST.get('totalValue')
    print(purchaseDetails)
    dataJSON = dumps(purchaseDetails)
    print(dataJSON)
    cp= Customer.objects.all()
    list=[]
    for p in cp:
        list.append(p.phone)
    context = {
        "date": datetime.datetime.now().date(),
        "purchaseItems": dataJSON,
        "purchaseDetails": purchaseDetails,
        "total": total,
        "head": "TRANSACTION",
        "list": list,
    }
    return render(request, 'system/submitDetails.html', context)


@login_required
def savePurchaseDetails(request):
    if request.method == 'POST':
    # store purchase details
        customerPhone = request.POST.get('phone')
        discountt = int(float(request.POST.get('offer', 0)))
        newTotal = request.POST.get('newVal', 0)
        try:
            customer_fk = Customer.objects.get(phone=customerPhone)
            mail = True
            purchase = Sales(total_price=int(float(newTotal)), customer=customer_fk, discount=discountt, created_by=request.user)
        except:
            purchase = Sales(total_price=int(float(newTotal)), discount=discountt, created_by=request.user)
            mail=False
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
        context = {
            "mail": mail,
        }
    return render(request, 'system/mailReceipt.html', context)

@login_required
def mailReceipt(request):
    sales = Sales.objects.last()
    sales_item = SalesItem.objects.filter(sales=sales.id)
    items_purchased= []
    for item in sales_item:
        i= Inventory.objects.get(pk=item.item.id)
        name = i.item_name
        rate = i.price
        unit = item.purchase_unit
        line_total = item.line_total
        list = [name, rate, unit, line_total]
        items_purchased.append(list)
    data={
        "id":sales.id,
        "date": sales.date_created,
        "total": sales.total_price,
        "customer": Customer.objects.get(pk=sales.customer_id).full_name,
        "list": items_purchased
    }
    subject = "Receipt"
    email_from = settings.EMAIL_HOST_USER
    email_to=Customer.objects.get(pk=sales.customer_id).email
    subject, from_email, to = subject, email_from, email_to
    html_message = render_to_string('receipt.html', data)
    plain_message = strip_tags(html_message)
    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    messages.success(request, 'Receipt was mailed successfully.')
    return render(request, 'system/mailReceipt.html')
