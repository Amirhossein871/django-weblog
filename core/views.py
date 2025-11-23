from django.shortcuts import render, redirect
from .models import ContactUsModel
from .forms import ContactUsForm
from django.contrib import messages


# Create your views here.

def about_us(request):
    return render(request, "core/about_us.html")


def contact_us(request):
    if request.method == "GET":
        form = ContactUsForm()
        return render(request, "core/contact_us.html", {"form": form})
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            email = form.cleaned_data.get("email")
            title = form.cleaned_data.get("title")
            message = form.cleaned_data.get("message")

            data = ContactUsModel(
                name=name,
                email=email,
                title=title,
                message=message,
            )
            data.save()
            messages.success(request, "پیام شما با موفقیت ثبت شد")
            return redirect("contact-us")

        messages.error(request, "مشکلاتی وجود دارد")
        return render(request, "core/contact_us.html", {"form": form})
