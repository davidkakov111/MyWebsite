from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ContactForm
from django.core.mail import EmailMessage


def homepage(request):
    return render(request, 'index.html')

def game(request):
    return render(request, 'game.html')

def aboutme(request):
    return render(request, 'aboutme.html')

def signup(request):
    if request.method == "GET":
        return render(request, "signup.html")
    elif request.method == "POST":
        email = request.POST.get("email")
        try:
            if User.objects.filter(email=email).exists():
                return render(request, "existingaccount.html")
            password = request.POST.get("password")
            password1 = request.POST.get("pasword")
            if password != password1:
                return render(request, "invalidpassword.html")
            user = User.objects.create_user(username=email, email=email, password=password)
            user.save()
            login(request, user)
            return render(request, "successfulsignup.html")
        except:
            return render(request, 'index.html')

def Login(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        try:    
            username = request.POST.get("email")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, 'successfullogin.html')
            else:
                return render(request, "unsuccessfullogin.html")
        except:
            return render(request, 'index.html')

def Logout(request):
    logout(request)
    return render(request, 'index.html')

def contact(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            theme = form.cleaned_data['themes']
            message = form.cleaned_data['message']
            contents1 = [
                "Name:", name, "Message:", message
            ]
            message_body1 = "\n".join(contents1)
            email_to_send1 = EmailMessage(
                subject = theme,
                body = message_body1,
                from_email= email, 
                to = ['kovacsdavid648@gmail.com'],
                reply_to= [email],
            )
            email_to_send1.send()
            contents2 = [
                f'Dear {name},', 'I have received your message, and I will respond shortly from the email address kovacsdavid648@gmail.com. Thank you in advance for your patience and understanding!', 'Best regards,', 'Kovács Dávid'
            ]
            message_body2 = "\n".join(contents2)
            email_to_send2 = EmailMessage(
                subject = "Auto-reply",
                body =   message_body2,
                from_email= 'kovacsdavid648@gmail.com', 
                to = [email],
                reply_to= ['kovacsdavid648@gmail.com'],
            )
            email_to_send2.send()
            return render(request, 'contact_response.html', {"name":name})
    return render(request, "contact.html", {'form':form})

