from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from applications.cart.models import Cart
from applications.products.models import Product


def cart_view(request):
    cart_obj, new = Cart.objects.get_or_new(request)
    return render(request, 'cart/cart_page.html', locals())


@require_POST
def cart_update(request):
    cart_obj, is_new = Cart.objects.get_or_new(request)
    product_id = request.POST.get('product_id')
    qs = Product.objects.filter(id=product_id)
    if qs.count() == 1:
        product_obj = qs.first()
        if product_obj not in cart_obj.products.all():
            cart_obj.products.add(product_obj)
        else:
            cart_obj.products.remove(product_obj)
        request.session['cart_items'] = cart_obj.products.count()
    return redirect('cart:cart-page')



# request.session.set_expiry(300) # 5 min
# print(request.session)
# print(dir(request.session))
# request.session['id'] = 10 # set data in session
# del request.session['id'] # delete data by key from session
