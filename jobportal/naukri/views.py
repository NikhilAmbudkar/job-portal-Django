from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from . models import DetailJob,DetailData,Profile
from . forms import DetailDataForms,UserProfileForm
from django.utils.crypto import get_random_string
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import authenticate,login,logout
import random,json
# Create your views here.



def index(request):
    return render(request,'index.html')

def home(request):
    query = request.GET.get('q', '')
    jobs=DetailJob.objects.all()
    if query:
        jobs = jobs.filter(
            Q(jname__icontains=query) | Q(location__icontains=query) | Q(skills__icontains=query)
        )
    return render(request,'home.html',{'jobs':jobs})

def details(request,pk):
    job=DetailJob.objects.get(id=pk)
    context={
        'job':job
    }
    return render(request,'details.html',context)

def create_data(request):
    if request.method=='POST':
        form=DetailDataForms(request.POST,request.FILES)
        if form.is_valid():
            application =form.save()
            send_mail(
                'Job Application Confirmation',
                f"Dear {application.fname} {application.lname},\n\nThank you for applying to the job. We have received your application and will review it shortly.",
                settings.DEFAULT_FROM_EMAIL,
                [application.email],
                fail_silently=False,
            )
            # messages.success(request,'Thank You For Submitting🤗🤗')
            return redirect('home')
            # return HttpResponse('thank you for submitting ')
        else:
            messages.error(request,'Something Wrong 🙄🙄')
            # return HttpResponse('Something Wrong')
    form=DetailDataForms()
    return render(request,'form.html',{'form':form})

# def profile(request):
#     user=request.user
#     return render(request,'profile.html',{'user':user})
# views.py

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')  
    
    return render(request, 'profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user, user=user)
        if form.is_valid():
            form.save()
            profile.bio = form.cleaned_data.get('bio', '')
            profile.profile_picture = form.cleaned_data.get('profile_picture', None)
            profile.birthdate = form.cleaned_data.get('birthdate', None)
            profile.mobile_number = form.cleaned_data.get('mobile_number', '')
            profile.save()

            return redirect('profile') 

    else:
        form = UserProfileForm(instance=user, user=user)

    return render(request, 'edit_profile.html', {'form': form})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        send_mail(
            f'Contact Form Message from {name}',
            message,  
            email,
            [settings.CONTACT_EMAIL], 
            fail_silently=False,
        )

        send_mail(
            'Thank you for contacting us!',
            'We have received your message and will get back to you shortly.',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        
        messages.success(request,'Your message has been sent successfully! We will get back to you soon.')
        return redirect('contact')
    return render(request, 'contact.html')

# def signup(request):
#     if request.method=='POST':
#         un=request.POST.get('un')
#         em=request.POST.get('em')
#         tel=request.POST.get('tel')
#         pw1=request.POST.get('pw1')
#         pw2=request.POST.get('pw2')
#         if pw1==pw2:
#             if User.objects.filter(username=un).exists():
#                 context={'msg':'User Already Exists..😢😢'}
#                 return render(request,'signup.html',context)
#             else:
#                 User.objects.create_user(
#                     username=un,
#                     email=em,
#                     password=pw1
#                 )
#                 context={'msg':'User Created Successfull🤩🤩'}
#                 return render(request,'index.html',context)
#         else:
#             context={'msg':'Password Not Match🤐🤐'}
#             return render(request,'signup.html',context)   
#     return render(request,'signup.html')


def login_view(request):
           
    # if not request.user.is_authenticated:
    #     messages.error(request, "It is not possible. You have to log in first.")
    #     return render(request, 'login.html')
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
         un=request.POST.get('un')
         pw=request.POST.get('pw')
         user=authenticate(request,username=un,password=pw)
         if user is not None:
             login(request,user)
             return redirect('home')
         else:
             return render(request,'login.html',{'msg':'Enter Valid Credentials🙄🙄'})
    return render(request,'login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def send_verification_email(email, verification_code):
    subject = "Your Verification Code"
    message = f"Your verification code is: {verification_code}"
    from_email = "your-email@example.com"  
    send_mail(subject, message, from_email, [email])

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        verification_code = request.POST.get('verification_code')
        action = request.POST.get('action')
        if User.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered.")
                return redirect('signup')
        if action == 'send_verification_code':
            if email:
                verification_code = get_random_string(length=6, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
                request.session['sent_verification_code'] = verification_code

                send_verification_email(email, verification_code)
                messages.success(request, "Verification code sent to your email.")
                return render(request, 'signup.html', {
                    'email': email, 
                    'username': username,
                    'password1': password1,
                    'password2': password2
                })

        if action == 'sign_up':
            if 'sent_verification_code' in request.session:
                sent_code = request.session['sent_verification_code']
                if verification_code != sent_code:
                    messages.error(request, "Invalid verification code.")
                    return redirect('signup')
            else:
                messages.error(request, "Please send the verification code first.")
                return redirect('signup')
            if password1 != password2:
                messages.error(request, "Passwords do not match.")
                return redirect('signup')
            
            
            # if User.objects.filter(username=username).exists():
            #     messages.error(request, "user is already registered.")
            #     return redirect('signup')
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            del request.session['sent_verification_code']

            messages.success(request, "User created successfully!")
            return redirect('signup')  

    else:
        return render(request, 'signup.html')


def validate_code(request):
    if request.method == "POST":
        data = json.loads(request.body)
        entered_code = data.get('verification_code')
        if 'sent_verification_code' in request.session:
            sent_code = request.session['sent_verification_code']
            if entered_code == sent_code:
                return JsonResponse({"success": True})  
            else:
                return JsonResponse({"success": False, "message": "The verification code is incorrect. Please try again."})

        return JsonResponse({"success": False, "message": "Verification code not found in session."})

otp_storage = {}

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email'].strip().lower()  
        print(f"Checking email: {email}") 

        user_exists = User.objects.filter(email=email).exists()
        print(f"User exists: {user_exists}") 

        if not user_exists:
            messages.error(request, 'Email does not exist!')
            return redirect('forgot_password')

        user = User.objects.get(email=email)
        print(f"User found: {user.username}") 
        otp = random.randint(100000, 999999)
        otp_storage[email] = otp
        send_mail(
            'Password Reset OTP',
            f'Your OTP is: {otp}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )
        request.session['email'] = email
        messages.success(request,'code sent to mail')
        return redirect('verify_otp')

    return render(request, 'forgot_password.html')

def verify_otp(request):
    email = request.session.get('email')
    if not email:
        return redirect('forgot_password')

    if request.method == 'POST':
        entered_otp = request.POST['otp']
        if email in otp_storage and str(otp_storage[email]) == entered_otp:
            messages.success(request,'code verified')
            return redirect('reset_password') 
        else:
            messages.error(request, 'Invalid OTP')
            return redirect('verify_otp')

    return render(request, 'verify_otp.html')


def reset_password(request):
    email = request.session.get('email')
    if not email:
        return redirect('forgot_password')

    if request.method == 'POST':
        new_password = request.POST['password']
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        messages.success(request, 'Password changed successfully! You can now log in.')
        return redirect('login')  

    return render(request, 'reset_password.html')
