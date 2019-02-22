from django.shortcuts import render


def cart_view(request):
    # print(request.session)
    # print(dir(request.session))
    # request.session['id'] = 10 # set data in session
    # del request.session['id'] # delete data by key from session
    id = request.session.get('id', 5) # get data from session
    print(id, 'session key')
    # request.session.set_expiry(300) # 5 min
    return render(request, 'cart/cart_page.html', locals())
