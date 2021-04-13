from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from membership.models import Customer
from .forms import UserUpdateForm
from inventory.models import *
from django.db.models import Sum
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from SalesInventory.utils import render_to_pdf

# Create your views here.
def home(request):
    return render(request, 'staff/home.html')


@login_required
def dashboard(request):
    customer = Customer.objects.filter(date_created__gte=datetime.date.today() - datetime.timedelta(days=30)).count()
    purchase = Sales.objects.filter(date_created__gte=datetime.date.today() - datetime.timedelta(days=30)).count()
    inventory = Inventory.objects.all().count()
    items_sold= SalesItem.objects.all().aggregate(Sum('purchase_unit'))['purchase_unit__sum']
    top_products= Inventory.objects.raw('select i.id, item_code, item_name, sum(s.purchase_unit) items_sold from inventory_inventory i join inventory_salesItem s on i.id = s.item_id join inventory_sales sales on sales.id=s.sales_id  group by i.id, item_code, item_name order by items_sold desc;')[:10]
    print(customer, purchase, inventory, items_sold)
    #Inventory.objects.raw('''select item_code, item_name, count(inventory.item_code) from inventory join salesItem on inventory.item_code=salesItem.item group by item_code desc''')
    context={
        "customerNo": customer,
        "purchaseNo": purchase,
        "inventoryNo": inventory,
        "itemSold": items_sold,
        "top_products": top_products,
        "head": "NAMASTE SALES AND INVENTORY - DASHBOARD",
    }

    # send offers to customers
    items = Inventory.objects.all().filter(in_stock__lte=5, status="C")
    offers = Offers.objects.filter(mail_date=datetime.datetime.now().date(), mail_status="pending")
    for offer in offers:
        subject = offer.mail_subject
        message = offer.mail_body
        email_from = settings.EMAIL_HOST_USER
        recipient_list = []
        customers=Customer.objects.all()
        for c in customers:
            recipient_list.append(c.email) # to all customers
        send_mail(subject, message, email_from, recipient_list)
        offer.mail_status="sent"
        offer.save()
    # view low stock alert to the admin
    if request.user.is_superuser:
        for i in items:
            msg = "WARNING: The stock quantity of " + i.item_name +" (Code: " +i.item_code+")"+" is "+ str(i.in_stock)+"."
            messages.warning(request, msg)
    return render(request, 'system/dashboard.html', context)

@login_required
def generate_view(request, *args, **kwargs):
    customer = Customer.objects.filter(date_created__gte=datetime.date.today() - datetime.timedelta(days=30)).count()
    purchase = Sales.objects.filter(date_created__gte=datetime.date.today() - datetime.timedelta(days=30)).count()
    inventory = Inventory.objects.all().count()
    newItems = Inventory.objects.filter(stocked_date__gte=datetime.date.today() - datetime.timedelta(days=30)).count()
    items_sold = SalesItem.objects.aggregate(Sum('purchase_unit'))['purchase_unit__sum']
    top_purchase = Sales.objects.all().order_by('-total_price')[:5]
    top_products= Inventory.objects.raw('select i.id, item_code, item_name, sum(s.purchase_unit) items_sold from inventory_inventory i join inventory_salesItem s on i.id = s.item_id join inventory_sales sales on sales.id=s.sales_id where sales.date_created  > CURRENT_DATE -30 group by i.id, item_code, item_name order by items_sold desc;')[:5]
    data={
        "from_date": datetime.date.today() - datetime.timedelta(days=30),
        "today": datetime.date.today(),
        "customerNo": customer,
        "purchaseNo": purchase,
        "newItems": newItems,
        "inventoryNo": inventory,
        "itemSold": items_sold,
        "top5": top_purchase,
        "top_products":top_products,
    }

    pdf = render_to_pdf('report.html', data)
    return HttpResponse(pdf, content_type='application/pdf')

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form,
        'head': "Profile Settings"
    }

    return render(request, 'staff/profile.html', context)

