# For Regex email validation
import re
import datetime
from main.models import User, UserCookie, NoPasswordWaitingForEmailConfirm
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
# Messages back if error
from django.contrib import messages
# Sending 403
from django.http import HttpResponseForbidden
# Notify Service
from main.notify import send_email

# import logging
from mama_cas.utils import to_bool
# from mama_cas.compat import is_authenticated
# from mama_cas.models import ServiceTicket
from mama_cas.views import LoginView
# logger = logging.getLogger(__name__)



def home(request):
    if request.user.is_authenticated:

        # NO RENDER
        # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # fileHandle = open(os.path.join(BASE_DIR, 'templates/account.html'), 'r') 
        # return HttpResponse(content=fileHandle.read(), content_type='text/html')

        context = {}
        return render(request, 'account.html', context)
    else:
        # Redirect to Login page
        return redirect('/login/')


        
def login_view(request):
    # GET request
    if request.method == 'GET':
        if request.user.is_authenticated:
            service = request.GET.get('service')
            if service:
                return LoginView.as_view()(request)
            return redirect('/home/')
        else:
            """
SET USER COOKIE HERE TOO
            """
            # Redirect to Login page
            return LoginView.as_view()(request)

    # POST request
    elif request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        if request.POST.get('password'):
            print(email)
            print(password)
            return LoginView.as_view()(request)

        else: # LOGIN WITH EMAIL
            # Check valid email
            if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                url = request.GET.get('service') # Get URL to forward onto
                confirmEmailHold = None # Create confirmEmailHold object

                if url:
                    confirmEmailHold = NoPasswordWaitingForEmailConfirm.objects.create(email=email, url=url)
                else:
                    confirmEmailHold = NoPasswordWaitingForEmailConfirm.objects.create(email=email)


                """
                SEND EMAIL VARIABLES
                """
                # Unique Key
                key = confirmEmailHold.key
                clickable_url = 'http://localhost:8080'

                # Try to send email
                subject = 'Just one more step!'
                recipient = email
                message = "You're almost done.\n" \
                    + "Click the link below in " +  confirmEmailHold.browser + " to activate your account.\n" \
                    + clickable_url + "/signin/?key=" + str(key) + "\n" \
                    + "Where is my password?\n" \
                    + "We doesn't make you remember yet another password. Just click the link and you’re in.\n" \
                    + "No password. Ever."

                if send_email(subject, recipient, message):
                    print('EMAIL SENT')
                    confirmEmailHold.email_sent = True

                    # Try to find a user with this email
                    user = None
                    try:
                        user = User.objects.get(email=email)
                        confirmEmailHold.user = user
                    except:
                        # No User found - save without user
                        pass

                    # Save confirmEmailHold
                    confirmEmailHold.save()

                    context = {
                        'email': email
                    }
                    # SET COOKIE
                    response = render(request, 'login_with_email.html', context)
                    response.set_cookie('cookie', value=confirmEmailHold.cookie, domain="localhost")
                    return response

                else:
                    msg = 'Unable to send email to: ' + email
                    messages.info(request, msg)
                    return render(request, 'login.html')

            else:
                msg = 'Invalid Email: ' + email
                messages.info(request, msg)
                return render(request, 'login.html')



@csrf_protect
@ensure_csrf_cookie
def signup(request):
    if request.user.is_authenticated:
        return redirect('/home/')

    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create(first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/home/')
            else:
                # Return a 'disabled account' error message
                print('Disabled Account')
    context = {}
    return render(request, "signup.html", context)


def loggedin(request):
    if request.user.is_authenticated:
        return HttpResponse('YES')
    else:
        return HttpResponse('NO')


def signin(request):
    if request.user.is_authenticated:
        return redirect('/home/')
        
    if request.method == 'GET':
        key = request.GET.get('key', None)
        print('key', key)

        if not key:
            return redirect('/login/')
        else:
            try:
                confirmEmailHold = NoPasswordWaitingForEmailConfirm.objects.get(key=key)
            except:
                # No key found
                return redirect('/login/')

            if confirmEmailHold.user:
                # USER EXISTS
                user = confirmEmailHold.user
                # Get Cookie
                cookie = request.COOKIES.get("cookie")
                # See if cookie matches
                if cookie == confirmEmailHold.cookie:
                    """
SET USER COOKIE HERE TOO
                    """
                    UserCookie.objects.create(user=user, cookie=cookie)

                    print('Success: ' + user.id)
                    if user.is_active:
                        # Log User in
                        login(request, user)
                        # Remove confirmEmailHold
                        confirmEmailHold.delete()
                        return redirect('/home/')
                else:
                    # Cookie Does not match
                    return redirect('/login/')

            # USER SIGNUP
            else:
                email = confirmEmailHold.email
                user = User.objects.create(email=email)
                # Make Random unusable password
                user.set_password()
                user.save()
                """
SET USER COOKIE HERE TOO
                """

                # if url == confirmEmailHold.url:
                #     print('forward on')

            
            
        
    return HttpResponseForbidden()


def oldkeys(request):
    if request.user.is_authenticated:
        return redirect('/home/')

    if request.method == 'GET':
        # holds = NoPasswordWaitingForEmailConfirm.objects.filter(date_time__lt=datetime.datetime.now() - datetime.timedelta(minutes=10))
        holds = NoPasswordWaitingForEmailConfirm.objects.filter(date_time__lt=datetime.datetime.now())

        total = holds.count()

        if holds.exists():
            holds.delete()
    
        return HttpResponse(str(total))

    # NOT GET REQUEST
    return HttpResponseForbidden()