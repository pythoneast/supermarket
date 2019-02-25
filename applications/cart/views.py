from django.shortcuts import render

from applications.cart.models import Cart


def cart_view(request):
    obj, new = Cart.objects.get_or_new(request)
    return render(request, 'cart/cart_page.html', locals())


# request.session.set_expiry(300) # 5 min
# print(request.session)
# print(dir(request.session))
# request.session['id'] = 10 # set data in session
# del request.session['id'] # delete data by key from session
