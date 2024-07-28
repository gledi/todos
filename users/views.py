import secrets

from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Activation
from .forms import RegistrationForm


User = get_user_model()


def register(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                phone=form.cleaned_data['phone'],
                is_active=False,
            )
            user.set_password(form.cleaned_data['password'])
            user.save()

            key = secrets.token_urlsafe(48)
            activation = Activation(user=user, activation_key=key)
            activation.save()

            message = activation.generate_email_message(request)
            message.send()

            return redirect('/')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', context={
        "form": form,
    })


def activate_user(request: HttpRequest, activation_key: str) -> HttpResponse:
    now = timezone.now()    # now = datetime.datetime.now(datetime.UTC)
    activation = Activation.objects.select_related('user').filter(
        is_used=False,
        activation_key=activation_key
    ).first()
    if activation is None:
        return HttpResponse("Activation key not found", status=418)
    time_passed = now - activation.created_at
    if time_passed.total_seconds() > 7 * 24 * 3600:
        return HttpResponse("Activation key expired", status=418)
    activation.user.is_active = True
    activation.user.save()
    activation.is_used = True
    activation.save()
    return redirect('login')


def profile(request):
    return render(request, 'users/profile.html')