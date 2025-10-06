from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.urls import reverse
import uuid
from app.models import User, Verification
import logging as logging
from utils.send_email_handler import send_email

logger = logging.getLogger(__name__)

### Auth User Views ###
def login_auth(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))
    if request.POST:
        username_or_email = request.POST.get('username_or_email', '')
        # Get remember me checkbox
        password = request.POST.get('password', '')
        remember_me = request.POST.get('remember')
        user = authenticate(
            request, username=username_or_email, password=password)
        if user is not None:
            try:
                verif = Verification.objects.get(user=user)
            except Verification.DoesNotExist:
                verif = None
            if verif and verif.verified == True:
                login(request, user)

                if remember_me:
                    # Set session to expire in 30 days instead of when browser closes
                    request.session.set_expiry(
                        30 * 24 * 60 * 60)  # 30 days in seconds

                    # Optional: Set a longer cookie age
                    request.session.cycle_key()  # Generate new session key for security
                else:
                    # Default behavior - session expires when browser closes
                    request.session.set_expiry(0)
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

    return render(request, 'app/templates/confirm.html', {'verified': False, 'email': email})


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

            send_email('Account Verification', email,
                       f'''Welcome!\n\nClick the following verification link to activate your account: \n<a target="_blank" href="{confirm_signup_link}?code={verif_code}&email={email}">Verify Account</a>''')
        elif not verification.verified:
            send_email('Account Verification', email,
                       f'''Welcome!\n\nClick the following verification link to activate your account: \n<a target="_blank" href="{confirm_signup_link}?code={verification.code}&email={email}">Verify Account</a>''')
        else:
            send_email('Account available', email, f'''Hello,\n\nYou already have an account on our platform. Please log in with your email and password.\nIf you forgot your password, please reset it.''')
            return render(request, 'app/templates/confirm.html', {'verified': True, 'option': 'signup'})
        return render(request, 'app/templates/confirm.html', {'email': email})
    email = request.GET.get('email', None)
    return render(request, 'app/templates/signup.html', {'email': email})


def reset_password_email(request):
    if request.POST:
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            verif = Verification.objects.filter(user=user).first()
            if verif.verified:
                code = str(uuid.uuid4())
                verif.code = code
                verif.save()
                reset_password_link = settings.PARENT_HOST + \
                    reverse('reset_password')+f'?email={email}&code={code}'
                if settings.PROD or settings.STAGING:
                    reset_password_link = 'https://' + reset_password_link
                else:
                    reset_password_link = 'http://' + reset_password_link
                print("Reset Password Link: ", reset_password_link)
                send_email('Reset Password', email,
                           f'''Click the following link to reset your password: \n<a target="_blank" href="{reset_password_link}">Reset Password</a>''')
            else:
                verification_link = settings.PARENT_HOST + \
                    reverse('confirm')+f'?email={email}&code={verif.code}'
                if settings.PROD or settings.STAGING:
                    verification_link = 'https://' + verification_link
                else:
                    verification_link = 'http://' + verification_link
                print("Email is not verified. Link: ", verification_link)
                send_email('Reset Password', email,
                           f'''Hello,\nYou requested to reset your password, but we noticed that your email has not been verified yet. Please click the following link to verify your email: \n<a target="_blank" href="{verification_link}">Verify Email</a>''')
        else:
            signup_link = settings.PARENT_HOST + \
                reverse('signup')+f'?email={email}'
            if settings.PROD or settings.STAGING:
                signup_link = 'https://' + signup_link
            else:
                signup_link = 'http://' + signup_link
            print("Email not registered. Link: ", signup_link)
            send_email('Reset Password', email,
                       f'''Hello,\nYou requested to reset your password, but we could not find your email. Please register your email here: \n<a target="_blank" href="{signup_link}">Register Email</a>''')
        return redirect(reverse('confirm')+'?email='+email)
    return render(request, 'app/templates/reset_password_email.html')


def reset_password(request):
    if request.GET:
        email = request.GET.get('email')
        code = request.GET.get('code')

        user = User.objects.filter(email=email).first()
        if user:
            verif = Verification.objects.filter(user=user).first()
            if verif.verified and code == verif.code:
                return render(request, 'app/templates/reset_password.html', {'verified': True, 'email': email})
    if request.POST:
        email = request.POST.get('email')
        user = User.objects.filter(email=email)
        if user:
            user = user[0]
            if 'confirm_password' in request.POST:
                password = request.POST.get('password')
                user.set_password(password)
                user.save()

                return render(request, 'app/templates/confirm.html', {'verified': True, 'option': 'reseted'})
            else:
                verif_code = str(uuid.uuid4())
                print("Reset Code: ", verif_code)
                verif = user.verification
                verif.code = verif_code
                verif.save()

                return render(request, 'app/templates/confirm.html', {'verified': True, 'option': 'reset'})

    return redirect('reset_password_email')
