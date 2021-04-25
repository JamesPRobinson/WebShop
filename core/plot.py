import pandas as pd
import numpy as np
import plotly.offline as opy
import plotly.graph_objs as pgo
from random import randint, sample
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

from .models import Item, Order, OrderItem, Address
from .plotutils import GetCategory, GetDiscount, GetLocation, GetQuantity, GetTotalSpent


MethodDict = {1: GetLocation, 2: GetTotalSpent,
              3: GetCategory, 4: GetDiscount, 5: GetQuantity}


def cluster(data):
    kmeans = KMeans(n_clusters=find_silhouette_score(data))
    Z = kmeans.fit_predict(data)
    return kmeans, Z

# Let the number of clusters be a parameter, so we can get a feel for an appropriate
# value thereof.


def find_silhouette_score(data):
    cluster_scores = []
    max_range = 15 if len(data) > 15 else len(data)
    for i in range(2, max_range):  # interate through potential clusters
        km = KMeans(n_clusters=i, random_state=42)
        cl_score = {}
        cl_score["num_clusters"] = i
        # Fit the KMeans model
        #
        km.fit_predict(data)

        #
        # Calculate Silhoutte Score
        #
        cl_score["score"] = silhouette_score(
            data, km.labels_, metric='euclidean')
        #
        cluster_scores.append(cl_score)
    avg_total_score = sum([e['score']
                           for e in cluster_scores]) / len(cluster_scores)
    clusters_by_score = sorted(cluster_scores,
                               key=lambda x: x['score'], reverse=True)
    num_clusters = clusters_by_score[0]['num_clusters']
    x, y = clusters_by_score[0], clusters_by_score[1]
    if (x['score'] - y['score']) < avg_total_score:
        num_clusters = x['num_clusters'] if x['num_clusters'] > y['num_clusters'] else y['num_clusters']
    return num_clusters


def get_graph(x, y):
    x, index = MethodDict[int(x)]()
    y, _ = MethodDict[int(y)]()
    # x, y, index = MethodDict[(x, y)]()
    dataset = np.array(list(zip(x, y))).reshape(len(x), 2)
    print(dataset)
    try:
        model, Z = cluster(dataset)
    except ValueError:
        return False
    # Represent fields, adding cluster information under color.
    trace0 = pgo.Scatter(x=x,
                         y=y,
                         text=index,
                         name='',
                         mode='markers',
                         marker=pgo.Marker(size=y,
                                           sizemode='diameter',
                                           sizeref=x.min(),
                                           opacity=0.75,
                                           color=Z),
                         showlegend=True
                         )
    # Represent cluster centers.
    trace1 = pgo.Scatter(x=model.cluster_centers_[:, 0],
                         y=model.cluster_centers_[:, 1],
                         name='',
                         mode='markers',
                         marker=pgo.Marker(symbol='x',
                                           size=12,
                                           color=[f"rgb({randint(0, 255)},{randint(0, 255)},{randint(0, 255)})" for e in range(model.n_clusters)]),
                         showlegend=True
                         )
    data = pgo.Data([trace0, trace1])
    layout = pgo.Layout(title='Results',
                        xaxis=pgo.layout.XAxis(showgrid=False,
                                               zeroline=False,
                                               showticklabels=False),
                        yaxis=pgo.layout.YAxis(showgrid=False,
                                               zeroline=False,
                                               showticklabels=False),
                        hovermode='closest'
                        )
    layout['title'] = 'Results'
    return pgo.Figure(data=data, layout=layout)
