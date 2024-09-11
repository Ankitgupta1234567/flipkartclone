from django.shortcuts import render,redirect,get_object_or_404
from .models import Products,Cart,Order
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic.list import ListView
from django.db.models import Q
from django.contrib import messages
import razorpay
import random
from django.conf import settings 
from django.core.mail import send_mail

# Create your views here.

def index(req):
    product=Products.objects.all()
    return render(req,"index.html",{"product":product})

class Productregister(CreateView):
    model=Products
    fields="__all__"
    success_url="/"

class Productlist(ListView):
    model=Products

def signup(req):
    if req.method == "POST":
        uname = req.POST["uname"]
        upass = req.POST["upass"]
        ucpass = req.POST["ucpass"]
        context = {}

        if uname == "" or upass == "" or ucpass == "":
            context["errmsg"] = "Field can't be empty"
            return render(req, "signup.html", context)
        elif upass != ucpass:
            context["errmsg"] = "Password and confirm password doesn't match"
            return render(req, "signup.html", context)
        else:
            try:
                userdata = User.objects.create(username=uname, password=upass)
                userdata.set_password(upass)
                userdata.save()
                return redirect("/signin")
            except:
                context["errmsg"] = "User Already exists"
                return render(req, "signup.html", context)
    else:
        context = {}
        context["errmsg"] = ""
        return render(req, "signup.html", context)


def signin(req):
    if req.method == "POST":
        uname = req.POST["uname"]
        upass = req.POST["upass"]
        context = {}
        if uname == "" or upass == "":
            context["errmsg"] = "Field can't be empty"
            return render(req, "signin.html", context)
        else:
            userdata = authenticate(username=uname, password=upass)
            if userdata is not None:
                login(req, userdata)
                return redirect("/")
            else:
                context["errmsg"] = "Invalid username and password"
                return render(req, "signin.html", context)
    else:
        return render(req, "signin.html")


def userlogout(req):
    logout(req)
    return redirect("/")

def moblielist(req):
    if req.method=="GET":
        allproducts=Products.productmanager.mobile_list()
        context={"product":allproducts}
        return render(req,"index.html",context)
    else:
        allproducts=Products.objects.all()
        context={"product":allproducts}
        return render(req,"index.html",context)
    

def electronicslist(req):
    if req.method=="GET":
        allproducts=Products.productmanager.electronics_list()
        context={"product":allproducts}
        return render(req,"index.html",context)
    else:
        allproducts=Products.objects.all()
        context={"product":allproducts}
        return render(req,"index.html",context)
    

def showpricerange(req):
    if req.method=="POST":
        r1=req.POST.get("min")
        r2=req.POST.get("max")
        if r1 and r2 :
            allproducts=Products.productmanager.pricerange(r1,r2)
            context={"product":allproducts}
            return render(req,"index.html",context)
        else:
            allproducts=Products.objects.all()
            context={"product":allproducts}
            return render(req,"index.html",context)

    else:
        return render(req,"index.html")
    
def sortingbyprice(req):
    sortoption=req.GET.get("sort")
    if sortoption=="low_to_high":
        product=Products.objects.order_by("price")
    elif sortoption=="high_to_low":
        product=Products.objects.order_by("-price")
    else:
        product=Products.objects.all()
    context={"product":product}
    return render(req,"index.html",context)

def searchproduct(req):
    query = req.GET.get("q")
    if query:
         
        products = Products.objects.filter(
            Q(productname__icontains=query) |
            Q(category__icontains=query) |
            Q(description__icontains=query)
        )
         
        if not products.exists():
            messages.info(req, "No results found for your query.")
    else:
        
        products = Products.objects.all()

    context = {"product": products}
    return render(req, "index.html", context)

def showcart(req):
    user=req.user
    allcarts=Cart.objects.filter(userid=user.id)
    totalamount=0
    for x in allcarts:
        totalamount+=x.productid.price*x.qty
    totalitems=len(allcarts)
    if req.user.is_authenticated:
        context={
            "allcarts":allcarts,
            "username":user,
            "totalamount":totalamount,
            "totalitems":totalitems
        }
    else:
        context={
            "allcarts":allcarts,
            "totalamount":totalamount,
            "totalitems":totalitems
        }


     
    return render(req,"showcart.html",context)

def updateqty(req,qv,productid):
    allcarts=Cart.objects.filter(productid=productid)
    if qv==1:
        total=allcarts[0].qty+1
        allcarts.update(qty=total)
    else:
        if allcarts[0].qty>1:
            total=allcarts[0].qty-1
            allcarts.update(qty=total)
        else:
            allcarts=Cart.objects.filter(productid=productid)
            allcarts.delete()
    return redirect("/showcart")
            
        
def removecart(req,productid):
    user=req.user
    cart=Cart.objects.filter(productid=productid,userid=user.id)
    cart.delete()
    return redirect("/showcart")

def addcart(req,productid):
    if req.user.is_authenticated:
        user=req.user
    else:
        user=None

    product=get_object_or_404(Products,productid=productid)
    cartitem,created=Cart.objects.get_or_create(productid=product,userid=user)
    if not created:
        cartitem.qty += 1
    else:
        cartitem.qty = 1
    cartitem.save()
    return redirect("/showcart")

    

def payment(req):
    if req.user.is_authenticated:
        user = req.user
        allcarts = Cart.objects.filter(userid=user.id)
        totalamount = 0
        for x in allcarts:
            orderid = random.randrange(1000, 90000)
            orderdata = Order.objects.create(
                orderid=orderid, productid=x.productid, userid=x.userid, qty=x.qty
            )
            orderdata.save()
            totalamount += x.qty * x.productid.price
            x.delete()

        oid = orderid

        client = razorpay.Client(
            auth=("rzp_test_wH0ggQnd7iT3nB", "eZseshY3oSsz2fcHZkTiSlCm")
        )
        data = {"amount": totalamount * 100, "currency": "INR", "receipt": str(oid)}
        payment = client.order.create(data=data)

        subject=f"Flipkart-payment status for your order={orderid}"
        msg=f'hi {user} , thank you for using our services.\n total amount plailds = rs.l {totalamount}/-'
        emailfrom=settings.EMAIL_HOST_USER
        receiver=[user,user.email]
        send_mail(subject,msg,emailfrom,receiver)

        context = {"data": payment, "amount": payment, "username": user}
        return render(req, "payment.html", context)
    else:
        return redirect("/signin")
    

def showorders(req):
    orderdata = Order.objects.filter(userid=req.user)
    totalamount = 0
    order_details = []
    
    for x in orderdata:
        order_total = x.qty * x.productid.price
        totalamount += order_total
        order_details.append({
            'order': x,
            'order_total': order_total
        })
    context = {
        "username": req.user,
        "orderdata": order_details,
        "totalamount": totalamount
    }

    return render(req, "showorders.html", context)