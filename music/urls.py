from django.urls import path,include
from . import views
app_name='music'

urlpatterns = [
    path('',views.home,name='home'),
    path('home',views.index,name='index'),
    path('premium', views.premium, name='premium'),
    path('<int:pk>',views.detail,name='detail'),
    path('premium/<int:pk>',views.pdetail,name='pdetail'),
    path('login',views.loginpage.as_view(),name='login'),
    path('signup',views.signup.as_view(),name='signup'),
    path('album/add',views.addalbum.as_view(),name='addalbum'),
    path('album/update/<int:pk>',views.updatealbum.as_view(),name='updatealbum'),
    path('album/delete/<int:pk>',views.deletealbum.as_view(),name='deletealbum'),
    path('logout',views.signout,name='signout'),
    path('song/add/<int:pk>',views.addsong.as_view(),name='addsong'),
    path('song/update/<int:pk>',views.updatesong.as_view(),name='updatesong'),
    path('song/delete/<int:pk>',views.deletesong.as_view(),name='deletesong'),
    path('search',views.search,name='search'),
    path('search1',views.search1,name='search1'),
    path("checkout/", views.checkout, name="Checkout"),
    path("handlerequest/", views.handlerequest, name="HandleRequest"),
    path("about/", views.about, name="aboutus"),
]
