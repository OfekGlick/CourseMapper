import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx


def what_can_i_take(course_ids: list, course_graph: nx.DiGraph):
    i_can_take = []
    for course in course_ids:
        i_can_take.append(nx.descendants(course_graph, int(course)))
    print("Drawing")
    i_can_take = set.intersection(*i_can_take)
    H = course_graph.subgraph(list(i_can_take))
    fig, ax = plt.subplots(1, 1, figsize=(50, 50))
    nx.draw(H, ax=ax)
    labels = nx.draw_networkx_labels(H, pos=nx.spring_layout(H))
    plt.show()
    return i_can_take

