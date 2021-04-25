
from .models import Item, Order, OrderItem, Address
import numpy as np
import pandas as pd
import random
from sklearn.preprocessing import LabelEncoder


def GetCategory():
    le = LabelEncoder()
    category_labels = [str(y.item.category) for x in Order.objects.all()
                       for y in x.items.all()]
    categories = [int(e) for e in le.fit_transform(category_labels).tolist()]
    return np.array(categories), category_labels


def GetDiscount():
    discount = [y.get_total_item_discount_price()
                for x in Order.objects.all() for y in x.items.all()]
    return np.array(discount), [f"Total Discount: {e}" for e in discount]


def GetLocation():
    le = LabelEncoder()
    country_labels = [str(e.address.country) for e in Order.objects.all()]
    countries = [int(e) for e in le.fit_transform(country_labels).tolist()]
    return np.array(countries), country_labels


def GetQuantity():
    quantity = [y.quantity
                for x in Order.objects.all() for y in x.items.all()]
    return np.array(quantity), [f"Order Quantity: {e}" for e in quantity]


def GetTotalSpent():
    total_spent = [e.get_total() for e in Order.objects.all()]
    return np.array(total_spent), [f"Total Spent: {e}" for e in total_spent]
