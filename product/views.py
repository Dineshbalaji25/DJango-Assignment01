from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductImage
from rest_framework import generics
from .serializers import ProductSerializer
from .forms import ProductForm

def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        images = request.FILES.getlist('images')  # ✅ Get multiple files

        if form.is_valid():
            product = form.save()
            for image in images:
                ProductImage.objects.create(product=product, image=image)
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form})

def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        images = request.FILES.getlist('images')

        if form.is_valid():
            form.save()
            for image in images:
                ProductImage.objects.create(product=product, image=image)
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_edit.html', {
        'form': form,
        'product': product,
        'images': product.images.all()
    })

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})



class ProductListCreateAPI(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailAPI(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
