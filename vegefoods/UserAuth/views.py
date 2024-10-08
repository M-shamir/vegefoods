from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.sessions.models import Session
from django.core.mail import send_mail
from django.conf import settings
from . models import  OTP
from django.contrib.auth.backends import ModelBackend
import random
from django.http import JsonResponse
from django.contrib.auth import login
import re
import random
from product_apps.models import Product
from wallet.models import Wallet
from cart_app.models import Cart,CartItem
from django.http import JsonResponse
from    . models import Message
from django.contrib import messages
from order_app.models   import Order,OrderItem
import google.generativeai as genai
import json
# Create your views here.


def redirect_to_home(request):
    return redirect('home')

def handle_not_found(request,exception):
    
    return render(request,'user/404page/404.html')

def count_cart(request):
    user = request.user
    if user.is_authenticated:
        try:
            # Get the user's cart
            cart = Cart.objects.get(user=user)
            # Count the number of unique products in the cart
            count_cartitems = cart.items.count()  # Use related_name 'items' to access cart items
        except Cart.DoesNotExist:
            count_cartitems = 0
    else:
        count_cartitems = 0

    return JsonResponse({'count': count_cartitems})

@never_cache
def user_home(request):
 
    username = request.user.username
    return render(request, 'user/index.html',{'username': username })


def user_registration(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        uname = request.POST.get('username')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        

        errors = {}
    
        if any(char.isdigit() or char.isspace() for char in uname):
            errors['username_error'] = 'Username should not contain numbers or spaces'

        
        if any(char.isdigit() or char.isspace() for char in first_name):
            errors['first_name_error'] = 'First name should not contain numbers or spaces'

        
        if any(char.isdigit() or char.isspace() for char in last_name):
            errors['last_name_error'] = 'Last name should not contain numbers or spaces'


        
        if User.objects.filter(username =  uname).exists():
            errors['username_error'] = 'Username already exists'


        if User.objects.filter(email =  email).exists():
            errors['email_error'] = 'Email is already exists'

        if pass1 != pass2:
            errors['password_error'] = 'Passwords do not match'

        if len(pass1) < 8:
            errors['password_error'] = 'Password must be at least 8 characters long'
        if not re.search(r'[A-Z]', pass1):
            errors['password_error'] = 'Password must contain at least one uppercase letter'
        if not re.search(r'[a-z]', pass1):
            errors['password_error'] = 'Password must contain at least one lowercase letter'
        if not re.search(r'[0-9]', pass1):
            errors['password_error'] = 'Password must contain at least one number'
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', pass1):
            errors['password_error'] = 'Password must contain at least one special character'
        if errors:
            return render(request,'user/signup.html', {'errors': errors})
        user = User.objects.create_user(username=uname, first_name=first_name, last_name=last_name, email=email, password=pass1)
        user.save()

        wallet = Wallet.objects.create(user=user,balance=0.00)
        wallet.save()

        otp = OTP(user=user)
        otp.save()
        send_otp_via_email(email, otp.otp_code)
        return redirect('verify_otp',user_id=user.id)

    return render(request, 'user/signup.html')

def send_otp_via_email(email, otp_code):
    subject = 'Your OTP Code'
    message = f'Your OTP code is {otp_code}.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


def resend_otp(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)
        otp_record = OTP.objects.get(user=user)

        # Generate new OTP
        new_otp = otp_record.generate_new_otp()
        send_otp_via_email(user.email, new_otp)

        return JsonResponse({'success': True, 'message': 'OTP resent successfully'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})




def verify_otp(request, user_id):
    if request.user.is_authenticated:
        return redirect('home')
    try:
        user = User.objects.get(id=user_id)
        if request.method == 'POST':
            entered_otp = request.POST.get('otp') 
            otp_record = OTP.objects.get(user=user)

        
            if otp_record.otp_code == entered_otp and otp_record.is_valid():
                user.is_active = True
                user.save()
                otp_record.delete() 

                login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                return redirect('home')
            else:
               
                return render(request, 'user/otp.html', {'error': 'Invalid OTP or OTP expired'})

    except User.DoesNotExist:
        return redirect('home')


    return render(request, 'user/otp.html')
@never_cache 
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        
        user = authenticate(request,username = username,password = pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return render(request,'user/login.html',{'error':'Username or Password is Wrong'})
    return render(request,'user/login.html')


def user_logout(request):
  
    logout(request)
    return redirect('home')



class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        if self.request.user.is_authenticated:
            return redirect('user_home') 
        email = form.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            return render(self.request, 'user/password_reset_form.html', {
                'form': form,
                'error': 'No account found with this email address.'
            })
        return super().form_valid(form)


def About_page(request):
    return render(request,'user/About/about.html')


def Contact_page(request):
    if request.method == 'POST':
       
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        subject = request.POST.get('complaint_subject')
        message = request.POST.get('message')

        new_message = Message(
            
            name = name,
            email = email,
            phone_number = phone_number,
            subject = subject,
            message = message,
            status='pending'
        )
        new_message.save()
        messages.success(request, "Message sent successfully! Our team will contact you within 10 minutes.")
        

        return redirect('contact')
    

    return render(request,'user/About/contact.html')

@login_required
def get_wallet_balance(request):
    try:
        wallet = Wallet.objects.get(user=request.user)
        balance = wallet.balance
        return JsonResponse({'balance': str(balance)})
    except Wallet.DoesNotExist:
        return JsonResponse({'error': 'Wallet not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def recipe_suggestions(request):
    try:
        genai.configure(api_key='AIzaSyA0EYygoQ-gdsUT-rR18QsDzP4g0yvzpR8')
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("Generate a list of 1 recipes with their names, descriptions, and YouTube video links. recipes want to include vegetables or fruits or juices or Dried fruits generates formats the data Adhere strictly to the given JSON Format")

        

        # Parse the response
        recipes =extract_json_from_text(response.text)

        # Ensure we have at least one recipe in the list
        if recipes and isinstance(recipes, list) and len(recipes) > 0:
            # Return all recipes as JSON
            return JsonResponse({'recipes': recipes})  # Return the full list

        else:
            return JsonResponse({'error': 'No recipes generated.'}, status=500)

    except json.JSONDecodeError:
        
        return JsonResponse({'error': 'Response is not valid JSON.'}, status=500)
    except Exception as e:
        
        return JsonResponse({'error': 'Failed to generate recipes.'}, status=500)


def extract_json_from_text(text):
    # Regular expression to find JSON-like structures in the text
    json_match = re.search(r"\[.*\]", text, re.DOTALL)
    
    if json_match:
        json_str = json_match.group()  # Extracted JSON string
        try:
            json_data = json.loads(json_str)  # Convert string to JSON (Python dictionary)
            return json_data
        except json.JSONDecodeError:
            pass
    else:
        pass
    return None
