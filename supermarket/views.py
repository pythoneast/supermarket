from django.shortcuts import render


def main_page(request):
    return render(request, 'index.html', locals())


def contacts(request):
    data = request.POST
    print(data)
    print(data.get('csrfmiddlewaretoken'))
    print(data.get('name'))
    print(data.get('email'))
    if 'gmail.com' not in data.get('email'):
        print('Only gmail accounts')
    return render(request, 'contacts.html', locals())
