import plotly.offline as opy
import plotly.graph_objs as go
from .models import Item, Order, OrderItem, Address


def FindValues():
    # one possible combination...is there a way of doing this more dynamically?
    result = {}
    # Country vs. Location
    countries = list(set([e.country for e in Address.objects.all()]))
    for i in range(len(countries)):
        result[i] = sum([e.get_total()
                         for e in Order.objects.all() if e.address.country == countries[i]])
    return result


def get_graph(x, y):
    results_dict = FindValues()
    x = list(results_dict.keys())
    y = list(results_dict.values())
    trace1 = go.Scatter(x=x, y=y, marker={'color': 'red', 'symbol': 104, 'size': 10},
                        mode="lines", name='1st Trace')

    data = go.Data([trace1])
    layout = go.Layout(title="Results", xaxis={
                       'title': 'x1'}, yaxis={'title': 'x2'})
    figure = go.Figure(data=data, layout=layout)
    return figure
