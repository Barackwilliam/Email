from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import EmailEntry
from .forms import EmailEntryForm

@login_required
def dashboard(request):
    search_query = request.GET.get('search', '')
    emails = EmailEntry.objects.filter(email__icontains=search_query)
    paginator = Paginator(emails, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dashboard.html', {'page_obj': page_obj, 'search_query': search_query})

@login_required
def add_email(request):
    if request.method == 'POST':
        form = EmailEntryForm(request.POST)
        if form.is_valid():
            email_entry = form.save(commit=False)
            email_entry.user = request.user
            email_entry.save()
            return redirect('dashboard')
    else:
        form = EmailEntryForm()
    return render(request, 'add_email.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def all_emails(request):
    user_emails = EmailEntry.objects.filter(user=request.user)
    return render(request, 'all_emails.html', {'user_emails': user_emails})

@login_required
def send_selected_emails(request):
    selected_ids = request.POST.getlist('selected_emails')
    selected_emails = EmailEntry.objects.filter(id__in=selected_ids)

    for email in selected_emails:
        message = render_to_string('email_template.html', {
            'email': email,
            'message_body': "This is a test email body. Customize as needed."
        })
        plain_message = strip_tags(message)
        send_mail('Subject: Important Message', plain_message, settings.DEFAULT_FROM_EMAIL, [email.email], html_message=message)

    return redirect('dashboard')

@login_required
def send_to_all_emails(request):
    emails = EmailEntry.objects.all()

    for email in emails:
        message = render_to_string('email_template.html', {
            'email': email,
            'message_body': "This is a test email body. Customize as needed."
        })
        plain_message = strip_tags(message)
        send_mail('Subject: Important Message', plain_message, settings.DEFAULT_FROM_EMAIL, [email.email], html_message=message)

    return redirect('dashboard')






from django.contrib import messages  # Hakikisha imewekwa juu

@login_required
def send_custom_message(request):
    if request.method == 'POST':
        message_body = request.POST.get('message_body')
        send_option = request.POST.get('send_option')
        selected_ids = request.POST.get('selected_ids').split(',') if request.POST.get('selected_ids') else []

        if send_option == 'selected':
            emails = EmailEntry.objects.filter(id__in=selected_ids)
        else:
            emails = EmailEntry.objects.all()

        sent_count = 0  # counter ya emails zilizotumwa

        for email in emails:
            message = render_to_string('email_template.html', {
                'email': email,
                'message_body': message_body
            })
            plain_message = strip_tags(message)
            send_mail('Custom Message', plain_message, settings.DEFAULT_FROM_EMAIL, [email.email], html_message=message)
            sent_count += 1

        messages.success(request, f'Message sent to {sent_count} email{"s" if sent_count != 1 else ""}.')
        return redirect('dashboard')

    else:
        user_emails = EmailEntry.objects.filter(user=request.user)
        return render(request, 'compose_message.html', {'user_emails': user_emails})

# @login_required
# def send_custom_message(request):
#     if request.method == 'POST':
#         message_body = request.POST.get('message_body')
#         send_option = request.POST.get('send_option')
#         selected_ids = request.POST.get('selected_ids').split(',') if request.POST.get('selected_ids') else []

#         if send_option == 'selected':
#             emails = EmailEntry.objects.filter(id__in=selected_ids)
#         else:
#             emails = EmailEntry.objects.all()

#         for email in emails:
#             message = render_to_string('email_template.html', {
#                 'email': email,
#                 'message_body': message_body
#             })
#             plain_message = strip_tags(message)
#             send_mail('Custom Message', plain_message, settings.DEFAULT_FROM_EMAIL, [email.email], html_message=message)

#         return redirect('dashboard')

#     else:
#         user_emails = EmailEntry.objects.filter(user=request.user)
#         return render(request, 'compose_message.html', {'user_emails': user_emails})



from django.core.paginator import Paginator
from django.contrib.auth.models import User

# @login_required
# def all_emails_by_user(request):
#     users = User.objects.all().prefetch_related('emailentry_set')
#     paginated_users = []

#     for user in users:
#         emails = user.emailentry_set.all()
#         paginator = Paginator(emails, 10)

#         # page key kwa kila user in unique format: page_userID
#         page_number = request.GET.get(f'page_{user.id}', 1)
#         page_obj = paginator.get_page(page_number)

#         paginated_users.append({
#             'user': user,
#             'page_obj': page_obj
#         })

#     return render(request, 'all_emails_by_user.html', {'paginated_users': paginated_users})


from django.contrib.auth.models import User  # Make sure this is imported
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def all_emails_by_user(request):
    users = User.objects.all()
    paginated_users = []

    for user in users:
        user_emails = EmailEntry.objects.filter(user=user)
        paginator = Paginator(user_emails, 5)
        page_number = request.GET.get(f'page_{user.id}')
        page_obj = paginator.get_page(page_number)

        paginated_users.append({
            'user': user,
            'page_obj': page_obj,
            'email_count': user_emails.count(),  # Count of emails
        })

    return render(request, 'all_emails_by_user.html', {'paginated_users': paginated_users})
