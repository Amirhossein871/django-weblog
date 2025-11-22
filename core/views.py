from django.shortcuts import render


# Create your views here.

def about_us(request):
    return render(request, "core/about_us.html")


def contact_us(request):
    if request.method == "GET":
        return render(request, "core/contact_us.html")
