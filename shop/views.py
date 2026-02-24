from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm
from accounts.utils import login_required


def product_list(request):
    q = request.GET.get('q', "").strip()
    page_number = request.GET.get('page', 1)

    products = Product.objects.all()

    if q:
        products = products.filter(Q(name__icontains=q))

    paginator = Paginator(products, 4)
    products = paginator.get_page(page_number)

    return render(request, "shop/product_list.html", {
        "products": products,
        "q": q,
    })

@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(request, "shop/product_form.html", {"form": form, "title": "Add product"})

@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)
    return render(request, "shop/product_form.html", {"form": form, "title": "Edit product"})

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect("product_list")
    return render(request, "shop/product_confirm_delete.html", {"product": product})
