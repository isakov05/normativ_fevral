from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import logout
from .forms import RegisterForm, LoginForm, ForgetPasswordForm, RestorePasswordForm
from .utils import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from .models import VerificationCode
from .utils import send_email_thread
from django.contrib.auth.models import User


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            group = Group.objects.get(name="User")
            user.groups.add(group)
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            login(request, user)
            return redirect("product_list")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

def forgot_password(request):
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, "Bunday foydalanuvchi topilmadi!")
                return redirect('forgot_password')

            code_obj = VerificationCode.objects.create(user=user)

            send_email_thread(
                subject="Parolni tiklash",
                message=f"Sizning kodingiz: {code_obj.code}\nKod 2 daqiqa ishlaydi.",
                recipient_email=user.email,
            )

            messages.success(request, "Emailingizga kod yuborildi!")
            return redirect('restore_password')
    else:
        form = ForgetPasswordForm()

    return render(request, 'registration/forgot_password.html', {'form': form})


def restore_password(request):
    if request.method == 'POST':
        form = RestorePasswordForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            new_password = form.cleaned_data['password']

            try:
                code_obj = VerificationCode.objects.filter(code=code).latest('id')
            except VerificationCode.DoesNotExist:
                messages.error(request, "Kod noto'g'ri!")
                return redirect('restore_password')

            if not code_obj.is_valid():
                messages.error(request, "Kodning muddati tugagan! Qaytadan so'rang.")
                return redirect('forgot_password')

            user = code_obj.user
            user.set_password(new_password)
            user.save()

            code_obj.delete()

            messages.success(request, "Parol muvaffaqiyatli yangilandi!")
            return redirect('login')
    else:
        form = RestorePasswordForm()

    return render(request, 'registration/restore_password.html', {'form': form})