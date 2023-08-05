import numpy as np


def first_order(graph, basis, typ="in"):
    clss = []
    for _ in np.arange(len(basis)+1):
        clss.append([])

    for node in graph.get_ids():
        fnd = False
        for i in np.arange(len(basis)):
            if node in basis[i]:
                fnd = True
                break
        if fnd:
            continue

        if typ == "in":
            cks = graph.get_in_degrees(node)
        else:
            cks = graph.get_out_degrees(node)

        for i in np.arange(len(basis)):
            for node_ in cks:
                if node_ in basis[i]:
                    fnd = True
                    clss[i].append(node)
                    break

            if fnd:
                break

        if fnd is False:
            clss[-1].append(node)
    return clss


def full_classification(graph, basis, typ="in"):
    return
