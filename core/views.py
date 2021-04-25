from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import DetailView, ListView, View, TemplateView, CreateView
from .forms import CheckoutForm, GraphChoiceForm
from .models import Item, Order, OrderItem, Address
from .plot import get_graph

# qs = query set


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

# Listview as we are listing out the items


class HomeView(ListView):
    model = Item
    template_name = 'home.html'
    paginate_by = 10  # number of items per page in ListView


def get_graph_choices(request):
    context = {}
    context['form'] = GraphChoiceForm()
    if request.GET:
        xfield = request.GET['x_field']
        yfield = request.GET['y_field']
        if xfield != yfield:
            fig = get_graph(xfield, yfield)
            if fig:
                graph = fig.to_html(
                    full_html=False, default_height=500, default_width=700)
                context['graph'] = graph
            else:
                messages.info(request, "Not enough data to process request")
        else:
            messages.info(request, "Fields must be unique")
    return render(request, "analytics.html", context)


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'order': order
            }

            address_qs = Address.objects.filter(
                user=self.request.user,
                default=True
            )
            if address_qs.exists():
                context.update({'default_address': address_qs[0]})
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order.")
            return redirect("core:home")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            # If order exists then we will check if the form submission is valid
            if form.is_valid():
                use_default_address = form.cleaned_data.get(
                    'use_default_address')
                if use_default_address:
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        default=True
                    )
                    if address_qs.exists:
                        address = address_qs[0]
                        order.address = address
                        order.save
                    else:
                        messages.info(
                            self.request, "No default address available"
                        )
                        return redirect('core:checkout')
                else:
                    street_address = form.cleaned_data.get('street_address')
                    apartment_address = form.cleaned_data.get(
                        'apartment_address')
                    country = form.cleaned_data.get('country')
                    post_code = form.cleaned_data.get('post_code')

                    if is_valid_form([street_address, country, post_code]):
                        address = Address(
                            user=self.request.user,
                            street_address=street_address,
                            apartment_address=apartment_address,
                            post_code=post_code,
                            country=country
                        )
                        address.save()
                        order.address = address
                        order.ordered = True
                        order.save()
                        set_default_address = form.cleaned_data.get(
                            'set_default_address'
                        )
                        if set_default_address:
                            address.default = True
                            address.save()
                        order_items = order.items.all()
                        order_items.update(ordered=True)
                        return redirect('core:home')
                    else:
                        messages.info(self.request,
                                      "Please fill in the required address fields")
                        return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "No active order found")
            return redirect('core:order-summary')
        messages.warning(self.request, form.errors)
        return redirect('core:checkout')


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "No active order found")
            return redirect('/')


class ProductDetailView(DetailView):
    model = Item
    template_name = 'product.html'


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False)
    # Order query set
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        # then grab the order from this query set
        order = order_qs[0]
        # check if the order item is in the order set
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, f"{str(item)} quantity updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, f"{str(item)} was added to your cart.")
            order.items.add(order_item)
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, f"{str(item)}was added to your cart.")
        return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    # get the item
    item = get_object_or_404(Item, slug=slug)
    # check the user has an order
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        # then grab the order from this query set
        order = order_qs[0]
        # check if the order item is in the order set
        # filter the item for that specific order slug
        if order.items.filter(item__slug=item.slug).exists():
            # grab order item
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False)[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, f"{str(item)} was removed from your cart.")
            return redirect("core:product", slug=slug)
        else:  # the order does not contain this order item
            messages.info(request, f"{str(item)} is not in your cart.")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "No orders currently in your cart.")
        return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, f"{str(item)} quantity updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, f"{str(item)} is not in your cart.")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)
