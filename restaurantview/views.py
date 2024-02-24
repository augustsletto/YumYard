from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils.timezone import datetime
from customerview.models import OrderModel, MenuItem
from .forms import MenuForm
from django.contrib import messages


class Dashboard(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        #get the current date
        today = datetime.today()
        orders = OrderModel.objects.filter(
            created_on__year=today.year, created_on__month=today.month, created_on__day=today.day)

        # loop through the orders and add the price value, check if order is not shipped
        unshipped_orders = []
        total_revenue = 0
        for order in orders:
            total_revenue += order.price

            if not order.is_shipped:
                unshipped_orders.append(order)

        # pass total number of orders and total revenue into template
        context = {
            'orders': unshipped_orders,
            'total_revenue': total_revenue,
            'total_orders': len(orders)
        }
            
        return render(request, 'restaurantview/dashboard.html', context)



    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()


class OrderDetails(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        context = {
            'order': order

        }

        return render(request, 'restaurantview/order-details.html', context)

    def post(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        order.is_shipped = True
        order.save()

        context = {
            'order': order
        }

        return render(request, 'restaurantview/order-details.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()




# Add restaurant items to menu
class AddMenu(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        form = MenuForm

        context = {
            'form': form
        }

        return render(request, 'restaurantview/add-menu.html', context)

    def post(self, request, *args, **kwargs):
        form = MenuForm
        if request.method == 'POST':
            form = MenuForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Item Added Successfully!')
            else:
                messages.error(request, 'Invalid Item')

            context = {
                'form': form
                }

        return render(request, 'restaurantview/add-menu.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()


# Edit restaurant menu
class EditMenu(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        menu_items = MenuItem.objects.all().order_by('-id')

        context = {
            'menu_items': menu_items
        }

        return render(request, 'restaurantview/edit-menu.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()


# Edit item in menu
# Follow along with Codemy.com
# https://www.youtube.com/watch?v=jCM-m_3Ysqk&t=793s
def edit_item(request, item_id):
    item = MenuItem.objects.get(pk=item_id)
    form = MenuForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        messages.success(request, 'Item Updated Successfully!')

    context = {
        'item': item,
        'form': form,
    }

    return render(request, 'restaurantview/edit-item.html', context)


# Delete item in menu
# Follow along with codemy.com
# https://www.youtube.com/watch?v=u1j-_kDc6g0&t=343s
def delete_item(request, pk):
    item = MenuItem.objects.get(pk=pk)
    item.delete()
    return render(request, 'restaurantview/dashboard.html')