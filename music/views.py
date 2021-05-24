from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from .models import Album,Song,Palbum, Plist, Orders, OrderUpdate
from django.views.generic import View,CreateView,UpdateView,DeleteView
from .myforms import Mylogin,Register,Addalbum,Addsong
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum
MERCHANT_KEY = 'your_merchant_key_here'
# Create your views here.

def index(request):
    a=Album.objects.all()
    if request.user.is_authenticated:
        return render(request,'music/home1.html',{'album':a})
    else:
        return render(request,'music/home.html',{'album':a})

def premium(request):
    a=Palbum.objects.all()
    if request.user.is_authenticated:
        return render(request,'music/phome1.html',{'album':a})
    else:
        return render(request,'music/phome.html',{'album':a})

def detail(request,pk):
    a=get_object_or_404(Album,pk=int(pk))
    context={'val':a}
    context['user']=request.user
    if request.user.is_authenticated:
        context['master']='music/master1.html'
        return render(request,'music/song.html',context)
    else:
        context['master'] = 'music/master.html'
        return render(request, 'music/song.html', context)

def pdetail(request,pk):
    a=get_object_or_404(Palbum,pk=int(pk))
    context={'val':a}
    context['user']=request.user
    if request.user.is_authenticated:
        context['master']='music/master1.html'
        return render(request,'music/plist.html',context)
    else:
        context['master'] = 'music/master.html'
        return render(request, 'music/plist.html', context)


class loginpage(View):
    def get(self,request):
        form=Mylogin(None)
        return render(request,'music/login.html',{'form':form})
    def post(self,request):
        form=Mylogin(request.POST or None)
        if form.is_valid():
            u=form.cleaned_data['UserName']
            p=form.cleaned_data['Password']
            v=authenticate(username=u,password=p)
            n=request.GET.get('next',None)
            print(n)
            if v is not None:
                login(request,v)
                if n:
                    return redirect(n)
                else:
                    return redirect('music:index')
        return render(request,'music/login.html',{'form':form})

class signup(CreateView):
    def get(self,request):
        form=Register(None)
        return render(request,'music/register.html',{'form':form})
    def post(self,request):
        form=Register(request.POST)
        if form.is_valid():
            data=form.save(commit=False)
            p=form.cleaned_data['Password']
            data.set_password(p)
            data.save()
            return redirect('music:login')
        return render(request,'music/register.html',{'form':form})


class addalbum(LoginRequiredMixin,CreateView):
    login_url = 'music:login'
    model = Album
    fields = ['title','artist','year','genre','image']
    template_name = 'music/addalbum.html'
    success_url = reverse_lazy('music:index')
    ''' Using normal View
    def get(self,request):
        form=Addalbum(None)
        return render(request,'music/addalbum.html',{'form':form})
    def post(self,request):
        form=Addalbum(request.POST,request.FILES)
        form.save()
        return redirect('music:index')'''


class updatealbum(LoginRequiredMixin,UpdateView):
    login_url = 'music:login'
    template_name = 'music/addalbum.html'
    model = Album
    fields = ['title','artist','genre','year','image']
    def form_valid(self, form):
        form.save()
        return redirect('music:index')

class deletealbum(LoginRequiredMixin,DeleteView):
    login_url = 'music:login'
    template_name = 'music/delete.html'
    model = Album
    success_url = reverse_lazy('music:index')

def signout(request):
    logout(request)
    return redirect('music:index')

class addsong(LoginRequiredMixin,CreateView):
    login_url = 'music:login'
    template_name = 'music/addsong.html'
    context_object_name = 'form'
    model = Song
    fields = ['title','artist','genre','sfile','image']
    def form_valid(self, form):
        i=self.kwargs.get('pk')
        a=Album.objects.get(pk=int(i))
        data=form.save(commit=False)
        data.al_id=a
        data.save()
        return redirect('music:detail',a.id)

class updatesong(LoginRequiredMixin,UpdateView):
    login_url = 'music:login'
    template_name = 'music/addsong.html'
    context_object_name = 'form'
    model=Song
    fields = ['title','artist','genre','sfile','image']
    def form_valid(self,form):
        form.save()
        a=Song.objects.get(id=int(self.kwargs.get('pk')))
        return redirect('music:detail',a.al_id.id)

class deletesong(LoginRequiredMixin,DeleteView):
    login_url = 'music:login'
    template_name = 'music/delete.html'
    model = Song
    def get_success_url(self):
        a=self.object.al_id
        return reverse_lazy('music:detail',kwargs={'pk':a.id})

def search(request):
    query=request.GET.get('search')
    print(query)
    if query:
        match=Album.objects.filter(title__startswith=query)
        print(match)
        if len(match)!=0:
            return render(request,'music/home.html',{'album':match})
        else:
            return render(request,'music/searchhome.html')

def search1(request):
    query=request.GET.get('search1')
    if query:
        match=Song.objects.filter(title__startswith=query)
        return render(request,'music/songsearch.html',{'val':match})


def home(request):
    return render(request,'music/mainhome.html')

def about(request):
    if request.user.is_authenticated:
        return render(request, 'music/aboutp.html')
    else:
        return render(request, 'music/about.html')

def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        # return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
        # Request paytm to transfer the amount to your account after payment by user
        param_dict = {

                'MID': 'Your_MID_here',
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'music/paytm.html', {'param_dict': param_dict})

    return render(request, 'music/checkout.html')


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'music/paymentstatus.html', {'response': response_dict})












