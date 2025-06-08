from django.shortcuts import render


def catalog_list(request):
    # TODO: Получить список товаров из БД
    products = []
    return render(request, 'catalog/list.html', {'products': products})

def product_detail(request, product_id):
    # TODO: Получить товар по ID
    return render(request, 'catalog/detail.html', {'product_id': product_id})
