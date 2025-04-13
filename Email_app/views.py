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
from django.db.models import Q



from datetime import datetime

@login_required
def dashboard(request):
    # Salamu ya wakati
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        greeting = "Good Morning"
    elif 12 <= current_hour < 17:
        greeting = "Good Afternoon"
    elif 17 <= current_hour < 22:
        greeting = "Good Evening"
    else:
        greeting = "Good Night"
    # Salamu ya wakati
    # Search & pagination logic (umeiweka tayari)
    search_query = request.GET.get('search', '')
    total_emails = EmailEntry.objects.count()

    if search_query:
        emails = EmailEntry.objects.filter(
            Q(email__icontains=search_query) |
            Q(region__icontains=search_query) |
            Q(district__icontains=search_query) |
            Q(school_name__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )
    else:
        emails = EmailEntry.objects.all()

    paginator = Paginator(emails, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    filtered_count = emails.count()

    return render(request, 'dashboard.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'total_emails': total_emails,
        'filtered_count': filtered_count,
        'greeting': greeting
    })




from django.contrib import messages
import random

success_messages = [
    "Great work, {username}! Your data has been successfully saved. Your contribution to the team is highly appreciated.",
    "Thank you, {username}. The school has been added successfully. Your collaboration is the cornerstone of our success.",
    "Well done, {username}! You have successfully added the data. We commend your consistent efforts.",
    "The data has been successfully saved. Thank you, {username}, for being part of our collective progress.",
    "Outstanding job, {username}! Keep up the great work – the team depends on you.",
    "Thank you for your contribution, {username}. You have successfully added a new school. Together, we are building a robust system.",
    "Your submission was successful. Thank you, {username}, for your wholehearted commitment to this task.",
    "Amazing work, {username}. The data has been saved successfully. We appreciate your hard work and dedication.",
    "Excellent job, {username}. The school has been added to the system. We’re grateful for your contribution.",
    "Your contribution is invaluable, {username}. The data has been saved, and we appreciate your commitment to excellence.",
    "Thank you for your dedication, {username}. The data has been added successfully. The team values your efforts.",
    "Great work, {username}! You’ve successfully submitted the data. We’re grateful for your efforts in making this a success.",
    "Well done, {username}. The school has been successfully added to the system. Your hard work is truly appreciated.",
    "Excellent contribution, {username}. Your data has been successfully recorded. We’re proud of your dedication.",
    "Thank you for your effort, {username}. The data has been added successfully. Keep up the excellent work.",
    "Great job, {username}. Your data has been added to the system. We are thankful for your contributions.",
    "You’ve done an excellent job, {username}. Your data has been successfully added to the system. We appreciate your hard work.",
    "Kudos, {username}. Your data has been successfully submitted. Thank you for your hard work and dedication.",
    "Well done, {username}. The data has been saved successfully. Keep up the great work – the team is counting on you.",
    "Fantastic job, {username}! You’ve successfully contributed. The team appreciates your hard work and effort.",
    "Great job, {username}. The data has been successfully saved. Your contribution is valued by the entire team.",
    "Thank you for your effort, {username}. The school has been successfully added. Your work makes a difference.",
    "Awesome work, {username}! Your contribution has been successfully saved. The team truly appreciates your dedication.",
    "Congratulations, {username}. You’ve added data successfully. We value your contribution to the project.",
    "Nice work, {username}. Your data has been successfully saved. The team is thankful for your hard work.",
    "Great work, {username}. The data has been successfully added. Your commitment to excellence is inspiring.",
    "Thank you, {username}. The school has been added successfully. We’re proud of your continuous effort.",
    "Amazing effort, {username}. The data has been successfully saved. Your work has made a significant impact.",
    "You did a fantastic job, {username}. Your data has been saved. Keep up the excellent work!",
    "Fantastic job, {username}. The data has been successfully added. The team is grateful for your dedication.",
    "Well done, {username}. The data has been successfully saved. Your contribution is helping us move forward.",
    "Great work, {username}. Your data has been successfully saved. Keep up the great work, and thank you for your effort.",
    "Excellent job, {username}. The data has been saved. Your contribution is essential to our progress.",
    "Congratulations, {username}. Your data has been successfully recorded. The team is grateful for your hard work.",
    "Well done, {username}. The data has been added successfully. We’re excited about the progress we’re making together.",
    "Fantastic work, {username}. The data has been successfully saved. The team is proud of what you’ve achieved.",
    "Thank you, {username}. Your contribution has been recorded successfully. Keep up the amazing work.",
    "Great work, {username}. You’ve successfully added the data. The team values your continued effort.",
    "You did an excellent job, {username}. Your data has been saved successfully. We’re grateful for your contribution.",
    "Awesome work, {username}. The data has been added successfully. Your efforts are helping build a better system.",
    "Nice work, {username}. Your data has been successfully added. The team appreciates your effort and dedication.",
    "Congratulations, {username}. You’ve successfully added the data. Your dedication is helping us grow.",
    "Outstanding job, {username}. The data has been saved successfully. We’re thankful for your consistent contributions.",
    "Well done, {username}. Your data has been successfully added. Keep pushing forward – the team is behind you.",
    "Fantastic job, {username}. The data has been saved successfully. You’re making a significant difference with your work.",
    "Excellent work, {username}. Your data has been successfully saved. We appreciate your consistent dedication.",
    "Great job, {username}. The data has been successfully added. Thank you for your continued efforts.",
    "Awesome effort, {username}. The data has been added successfully. Your hard work is appreciated.",
    "Well done, {username}. The data has been successfully saved. We’re thankful for your contribution to the system.",
    "Congratulations, {username}. Your data has been added successfully. Your efforts are driving the project forward.",
    "Thank you for your contribution, {username}. The data has been successfully recorded. Keep up the great work."
]



@login_required
def add_email(request):
    if request.method == 'POST':
        form = EmailEntryForm(request.POST)
        if form.is_valid():
            email_entry = form.save(commit=False)
            email_entry.user = request.user
            email_entry.save()

            # Chagua ujumbe mmoja randomly
            msg = random.choice(success_messages).format(username=request.user.username)
            messages.success(request, msg)

            return redirect('all_emails')
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
    
from django.core.paginator import Paginator

@login_required
def all_emails(request):
    user_emails = EmailEntry.objects.filter(user=request.user)
    total_user_emails = user_emails.count()

    paginator = Paginator(user_emails, 6)  # Emails 6 kwa kila page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'all_emails.html', {
        'page_obj': page_obj,
        'total_user_emails': total_user_emails
    })

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


from django.contrib.auth.models import User  # Make sure this is imported

@login_required
def all_emails_by_user(request):
    users = User.objects.all()
    paginated_users = []

    for user in users:
        user_emails = EmailEntry.objects.filter(user=user)
        paginator = Paginator(user_emails, 4)
        page_number = request.GET.get(f'page_{user.id}')
        page_obj = paginator.get_page(page_number)

        paginated_users.append({
            'user': user,
            'page_obj': page_obj,
            'email_count': user_emails.count(),  # Count of emails
        })

    return render(request, 'all_emails_by_user.html', {'paginated_users': paginated_users})
