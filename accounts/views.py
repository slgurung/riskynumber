from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from accounts.models import UserProfile
from watchlist.models import WatchList

# Create your views here.

# class SignUp(CreateView):
#
#     form_class = forms.NewUserForm
#     success_url = reverse_lazy('index.html') # reverse_lazy redirect to login only after pressing submit button
#     template_name = 'accounts/signup.html'

# for signin without ajax
######################
# def signin(request):
#     if request.method == 'POST':
#         username = request.POST.get('login_username') #return username
#         password = request.POST.get('login_password')
#
#         user = authenticate(username=username, password=password)
#
#         if user:
#             if user.is_active:
#                 login(request, user)
#                 return redirect('home')
#             else:
#                 return HttpResponse("account not active")
#         else:
#
#             return HttpResponse("invalid login credentials!")
#
#     else:
#         return render(request, 'accounts/login.html')

# login with ajax call
def signin(request):
    data = {}
    if request.method == 'POST':
        username = request.POST.get('uname') #return username
        password = request.POST.get('pword')
        user = authenticate(username = username, password = password)

        if user:
            if user.is_active:
                login(request, user)
                #return HttpResponseRedirect(reverse('home'))
                data['result'] = 'success'
                return JsonResponse(data)
            else: # make this better
                data['result'] = 'disabled.'
                return JsonResponse(data)
        else:   #elif user == None:
            #print('Invalid login details: {0}, {1}'.format(username, password))
            data['result'] = 'declined'
            return JsonResponse(data)
    data['result'] = 'get'
    return JsonResponse(data)

# to check username availability thru ajax
def validate_username(request):
    username = request.POST.get('uname')
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'Username: "' + username + '"' + ' is taken. Create another.'
    return JsonResponse(data)

#signup views from template form action attribute
def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name') #return username
        last_name = request.POST.get('last_name')
        username = request.POST.get('username') #return username
        password = request.POST.get('password')
        password2 = request.POST.get('password2') #return username
        email = request.POST.get('email')

        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, password=password, email=email)
        return redirect('home')
    else:
        return render(request, 'accounts/signup.html')
# signup views using ajax, without form action attribute
def signup_ajax(request):
    data = {}
    if request.method == 'POST':
        username = request.POST.get('uname') #return username
        password = request.POST.get('pword')
        password2 = request.POST.get('pword2') #return username
        first_name = request.POST.get('fname') #return username
        last_name = request.POST.get('lname')
        email = request.POST.get('email')

        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, password=password, email=email)
        # creates watchlist of new user
        watchlist_obj = WatchList(user=user)
        watchlist_obj.save()
        data['result'] = 'success'
        return JsonResponse(data)
    else:
        data['result'] = 'fail'
        return JsonResponse(data)

class ProfileView(ListView):
    model = UserProfile
    template_name = 'accounts/profile.html'
