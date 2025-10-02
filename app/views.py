from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django_hosts.resolvers import reverse
import uuid
from .models import User, Verification, Event
from utils.mail import send_email
import logging as logging

logger = logging.getLogger(__name__)


@login_required
def dashboard(request, content_type='dashboard'):
    return render(request, 'app/templates/app-dashboard.html', {content_type: True})

@login_required
def create_and_manage_events(request, id=None):
    user = request.user
    event = {'id': ''}
    if id:
        event = Event.objects.filter(id=id).first()
        
    if request.POST:
        if not id:
            event = Event.objects.create(user=user)
        event.title = request.POST.get('name')
        event.date_start = request.POST.get('date_start')
        event.date_end = request.POST.get('date_end')
        event.status = request.POST.get('status')
        event.description = request.POST.get('description')
        event.save()
        
        return redirect(reverse('events'))
    return render(request, 'app/templates/manage-events-drawer.html', {'events': True, 'event': event})

@login_required
def events_table(request):
    user = request.user
    events = Event.objects.filter(user=user).order_by('-created_at')
    return render(request, 'app/templates/events-table.html', {'events': events})

@login_required
def dashboard_content(request):
    user = request.user
    events = Event.objects.filter(user=user).order_by('date_start')
    return render(request, 'app/templates/app-dashboard-content.html', {'dashboard': True, 'events': events})


### Auth User Views ###
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
