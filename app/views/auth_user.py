from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.urls import reverse
import uuid
from app.models import User, Verification
import logging as logging

logger = logging.getLogger(__name__)

### Auth User Views ###
def login_auth(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))
    if request.POST:
        username_or_email = request.POST.get('username_or_email', '')
        password = request.POST.get('password', '')
        user = authenticate(
            request, username=username_or_email, password=password)
        if user is not None:
            try:
                verif = Verification.objects.get(user=user)
            except Verification.DoesNotExist:
                verif = None
            if verif and verif.verified == True:
                login(request, user)
            return redirect(reverse('dashboard'))
        else:
            return render(request, 'app/templates/login.html', {'username_or_email': username_or_email, 'error_message': 'Invalid email or password.'})
    return render(request, 'app/templates/login.html')


def confirm(request):
    verif_code = request.GET.get('code')
    email = request.GET.get('email')

    user = User.objects.filter(email=email).first()
    if user:
        verif = Verification.objects.filter(user=user).first()
        print(verif.code)
        if verif_code == verif.code:
            verif.verified = True
            verif.save()
            return render(request, 'app/templates/confirm.html', {'verified': True, 'option': 'signup'})

    return render(request, 'app/templates/confirm.html')


@login_required
def signout(request):
    if not request.user.is_authenticated:
        return redirect(reverse('landing_page'))

    logout(request)
    return redirect(reverse('landing_page'))


def signup(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))

    if request.POST:
        email = request.POST.get('email')
        username = request.POST.get('username')
        role = request.POST.get('sign_as')
        address = request.POST.get('address')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        verif_code = str(uuid.uuid4())[:5]
        logger.info("Verification code: %s", verif_code)

        if confirm_password != password:
            return render(request, 'app/templates/signup.html', {'error_message': 'Password is incorrect.'})

        try:
            user = User.objects.get(email=email)
            error_message = 'Email already registered. Please use another email.'
            return render(request, 'app/templates/signup.html', {'error_message': error_message})
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=username)
                error_message = 'Username already taken. Please choose another username.'
                return render(request, 'app/templates/signup.html', {'email': email, 'error_message': error_message})
            except User.DoesNotExist:
                user = User.objects.create_user(
                    email=email,
                    username=username,
                    first_name=username,
                    password=password
                )
            except User.MultipleObjectsReturned:
                first_user = User.objects.filter(
                    email=email).order_by('-created_at').first()
                User.objects.filter(email=email).exclude(
                    id=first_user.id).delete()
                user = first_user
        except User.MultipleObjectsReturned:
            error_message = 'Email already registered. Please use another email.'
            return render(request, 'app/templates/signup.html', {'email': email, 'error_message': error_message})

        verification = Verification.objects.filter(user=user).first()
        
        # For Email way verification
        confirm_signup_link = settings.PARENT_HOST + reverse('confirm')
        if settings.DEBUG:
            confirm_signup_link = 'http://' + confirm_signup_link
        else:
            confirm_signup_link = 'https://' + confirm_signup_link
        if not verification:
            verification, _ = Verification.objects.get_or_create(user=user)
            verification.verified = False
            verification.address = address
            verification.role = role
            verification.code = verif_code
            verification.save()
        else:
            return render(request, 'app/templates/confirm.html', {'verified': True, 'option': 'signup'})
        context = {
            'verification_code': verif_code,
            'email': email
        }
        return render(request, 'app/templates/confirm.html', context)
    email = request.GET.get('email', None)
    return render(request, 'app/templates/signup.html', {'email': email})
