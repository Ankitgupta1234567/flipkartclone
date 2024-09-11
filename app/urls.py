 
from django.urls import path
from . import views
from app.views import Productlist,Productregister

urlpatterns = [
    path("",views.index,name="index")   ,
    path("signin/",views.signin,name="signin"),
    path("signup/",views.signup,name="signup"),
    path("userlogout/",views.userlogout,name="userlogout"),
    path("Productregister",Productregister.as_view(),name="Productregister"),
    path("Productlist/",Productlist.as_view(),name="Productlist"),
    path("mobilelist/",views.moblielist,name="moblielist"),
    path("electronicslist/",views.electronicslist,name="electronicslist"),
    path("showpricerange/",views.showpricerange,name="showpricerange"),
    path("sortingbyprice/",views.sortingbyprice,name="sortingbyprice"),
    path("searchproduct/",views.searchproduct,name="searchproduct"),
    path("searchproduct/",views.searchproduct,name="searchproduct"),
    path("showcart/",views.showcart,name="showcart"),
    path("updateqty/<int:qv>/<int:productid>/",views.updateqty,name="updateqty"),
    path("removecart/<int:productid>/",views.removecart,name="removecart"),
    path("addcart/<int:productid>/",views.addcart,name="addcart"),
    path("payment/",views.payment,name="payment"),
    path("showorders/",views.showorders,name="showorders"),



]