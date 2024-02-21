from django.shortcuts import render
from django.views import View
from django.core.mail import send_mail
from .models import MenuItem, Category, OrderModel


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customerview/index.html')


class About(View):
    def get (self, request, *args, **kwargs):
        return render(request, 'customerview/about.html')


class Order(View):
    def get(self, request, *args, **kwargs):
        # Get every item from each category
        appetizers = MenuItem.objects.filter(category__name__contains='Appetizer')
        entres = MenuItem.objects.filter(category__name__contains='Entre')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')
        
        

        # Pass into context
        context = {
            'appetizers': appetizers,
            'entres': entres,
            'desserts': desserts,
            'drinks': drinks,

        }


        # Render into template
        return render(request, 'customerview/order.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code
        )
        order.items.add(*item_ids)

        # After everything is done, send confirmation email to the user

        body = ('Thank you for your order! Your food is being made and will be dealivered soon!\n'
        f'Your total: {price}\n'
        'Thank you again for your order!')

        send_mail(
            'Thank you for your order!',
            body,
            'example@example.com',
            [email],
            fail_silently=False
        )

        context = {
            'items': order_items['items'],
            'price': price
        }

        return render(request, 'customerview/order_confirmation.html', context)