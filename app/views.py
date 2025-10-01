from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django_hosts.resolvers import reverse
import uuid
from .models import User, Verification
from utils.mail import send_email
import logging as logging

logger = logging.getLogger(__name__)

@login_required
def event_input(request):
    return render(request, 'app/templates/dashboard.html', {'events': True})

@login_required
def dashboard(request):
    return render(request, 'app/templates/dashboard.html', {'dashboard': True})


def login_auth(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))
    if request.POST:
        email = request.POST.get('email','')
        password = request.POST.get('password', '')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            try:
                verif = Verification.objects.get(user=user)
            except Verification.DoesNotExist:
                verif = None
            if verif and verif.verified == True:
                login(request, user)
            return redirect(reverse('dashboard'))
        else:
            return render(request, 'app/templates/login.html', {'email': email, 'error_message': 'Invalid email or password.'})
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
                           f'Click the link to change your password: \n{reset_password_link}')
            else:
                link_verifikasi = settings.PARENT_HOST + \
                    reverse('confirm')+f'?email={email}&code={verif.code}'
                if settings.PROD or settings.STAGING:
                    link_verifikasi = 'https://' + link_verifikasi
                else:
                    link_verifikasi = 'http://' + link_verifikasi
                print("Email belum terverifikasi. Link: ", link_verifikasi)
                send_email('Reset Password', email,
                           f'Halo,\nAnda ingin melakukan pengaturan kata sandi Anda, namun kami melihat bahwa Anda belum menyelesaikan verifikasi email. Klik tautan berikut untuk melakukan verifikasi: \n{link_verifikasi}')
        else:
            signup_link = settings.PARENT_HOST + \
                reverse('signup')+f'?email={email}'
            if settings.PROD or settings.STAGING:
                signup_link = 'https://' + signup_link
            else:
                signup_link = 'http://' + signup_link
            print("Email belum terdaftar. Link: ", signup_link)
            send_email('Reset Password', email,
                       f'Halo,\nAnda ingin melakukan pengaturan kata sandi Anda, namun kami tidak menemukan email Anda. Daftarkan email Anda di sini: \n{signup_link}')
        return redirect(reverse('confirm')+'?email='+email)
    return render(request, 'reset_password_email.html')


def reset_password(request):
    if request.GET:
        email = request.GET.get('email')
        code = request.GET.get('code')

        user = User.objects.filter(email=email).first()
        if user:
            verif = Verification.objects.filter(user=user).first()
            if verif.verified and code == verif.code:
                return render(request, 'reset_password.html', {'verified': True, 'email': email})
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


@login_required
def signout(request):
    if not request.user.is_authenticated:
        return redirect(reverse('index'))

    logout(request)
    return redirect(reverse('index'))


def signup(request):
    print(request.POST)
    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))

    if request.POST:
        email = request.POST.get('email')
        username = request.POST.get('username')
        address = request.POST.get('address')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        verif_code = str(uuid.uuid4())[:5]
        logger.info("Verification code: %s", verif_code)

        if confirm_password != password:
            return render(request, 'app/templates/signup.html', {'error_message': 'Password is incorrect.'})

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=username)
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
                User.objects.filter(email=email).exclude(id=first_user.id).delete()
                user = first_user
        except User.MultipleObjectsReturned:
            first_user = User.objects.filter(
                email=email).order_by('-created_at').first()
            User.objects.filter(email=email).exclude(id=first_user.id).delete()
            user = first_user
        verification = Verification.objects.filter(user=user).first()
        confirm_signup_link = settings.PARENT_HOST + reverse('confirm')
        confirm_signup_link = 'http://' + confirm_signup_link
        if not verification:
            verification, _ = Verification.objects.get_or_create(user=user)
            verification.verified = False
            verification.address = address
            verification.code = verif_code
            verification.save()

            send_email('Account Verification', email,
                       f'Welcome!\n\nClick the following verification link to activate your account: \n{confirm_signup_link}?code={verif_code}&email={email}')
        elif not verification.verified:
            send_email('Account Verification', email,
                       f'Welcome!\n\nClick the following verification link to activate your account: \n{confirm_signup_link}?code={verification.code}&email={email}')
        else:
            send_email('Account Available', email,
                       f'Hello,\n\nYou already have an account on our platform. Please log in with your email and password.\nIf you forgot your password, please reset your password.')
            return render(request, 'app/templates/confirm.html', {'verified': True, 'option': 'signup'})
        context = {
            'verification_code': verif_code,
            'email': email
        }
        return render(request, 'app/templates/confirm.html', context)
    email = request.GET.get('email', None)
    return render(request, 'app/templates/signup.html', {'email': email})
