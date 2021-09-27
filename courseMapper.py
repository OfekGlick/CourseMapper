import matplotlib.pyplot as plt
import networkx as nx


def what_can_i_take(course_ids: list, course_graph: nx.DiGraph):
    i_can_take = []
    i_took = []
    for course in course_ids:
        # i_took.append(set(course))
        # i_can_take.append({course})
        # i_took.append(set(list(zip(*course_graph.out_edges(int(course))))[1]))
        i_can_take.append(set(list(zip(*course_graph.in_edges(int(course))))[0]))
    print("Drawing")
    course_ids = [int(course) for course in course_ids]
    i_can_take = set.union(*i_can_take)
    i_can_take = i_can_take.union(set(course_ids))
    H = course_graph.subgraph(list(i_can_take))
    print(H.edges)
    fig, ax = plt.subplots(1, 1, figsize=(20, 20))
    nx.draw(H, ax=ax)
    labels = nx.draw_networkx_labels(H, pos=nx.spring_layout(H))
    plt.savefig('DSCourses.png')
    plt.show()
    # return i_can_take

