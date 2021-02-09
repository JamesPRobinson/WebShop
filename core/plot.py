import plotly.offline as opy
import plotly.graph_objs as go


def get_graph():
    x = [-2, 0, 4, 6, 7]
    y = [q**2 - q + 3 for q in x]
    trace1 = go.Scatter(x=x, y=y, marker={'color': 'red', 'symbol': 104, 'size': 10},
                        mode="lines", name='1st Trace')

    data = go.Data([trace1])
    layout = go.Layout(title="Meine Daten", xaxis={
                       'title': 'x1'}, yaxis={'title': 'x2'})
    figure = go.Figure(data=data, layout=layout)
    return figure
