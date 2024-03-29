import json
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import View
from django.urls import reverse
from django.db.models import Q
from django.core.mail import send_mail
from .models import MenuItem, Category, OrderModel, Restaurant
from .forms import ContactForm



class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customerview/index.html')



def contact(request):
    submitted = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(cd['subject'], cd['message'], cd.get(
                'email', 'noreply@example.com'), ['contact@yum.com'])

        return HttpResponseRedirect(reverse('contact') + '?submitted=True')
    else:
        form = ContactForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'customerview/contact.html',
                  {'form': form, 'submitted': submitted})


class Restaurants(View):
    def get(self, request, *args, **kwargs):
        restaurants = Restaurant.objects.all()

        context = {
            'restaurants': restaurants
        }

        return render(request, 'customerview/restaurants.html', context)




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
        sandwiches = MenuItem.objects.filter(category__name__contains='Sandwich')
        salads = MenuItem.objects.filter(category__name__contains='Salad')
        burgers = MenuItem.objects.filter(category__name__contains='Burgers')
        sushi = MenuItem.objects.filter(category__name__contains='Sushi')
        pasta = MenuItem.objects.filter(category__name__contains='Pasta')
        pizza = MenuItem.objects.filter(category__name__contains='Pizza')
        

        # Pass into context
        context = {
            'appetizers': appetizers,
            'entres': entres,
            'desserts': desserts,
            'drinks': drinks,
            'sandwiches': sandwiches,
            'salads': salads,
            'burgers': burgers,
            'sushi': sushi,
            'pasta': pasta,
            'pizza': pizza,
}


        # Render into template
        return render(request, 'customerview/order.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        street = request.POST.get('street')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip')

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
            phone_number=phone_number,
            street=street,
            city=city,
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

        return redirect('order-confirmation', pk=order.pk)


class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,
        }


        return render(request, 'customerview/order_confirmation.html', context)

    def post(self, request ,pk, *args, **kwargs):
        data = json.loads(request.body)

        if data['isPaid']:
            order = OrderModel.objects.get(pk=pk)
            order.is_paid = True
            order.save()


        return redirect('payment-confirmation')

class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customerview/order_pay_confirmation.html')

    

class Menu(View):
    def get(self, request, *args, **kwargs):
        menu_items = MenuItem.objects.all()

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customerview/menu.html', context)


class Profile(View):
    def get(self, request, *args, **kwargs):

        return render(request, 'customerview/profile.html')


class Cart(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customerview/cart.html')



class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        menu_items = MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query)
        )

        context = {
            'menu_items': menu_items

        }

        return render(request, 'customerview/menu.html', context)



