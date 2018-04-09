"""A class for the Lemke Howson algorithm"""
from nash.integer_pivoting import (make_tableau, non_basic_variables,
                                   pivot_tableau)

import warnings

import numpy as np
from itertools import cycle
import matplotlib.pyplot as plt
import time

def shift_tableau(tableau, shape):
    """
    Shift a tableau to ensure labels of pairs of tableaux coincide

    Parameters
    ----------

        tableau: a numpy array
        shape: a tuple

    Returns
    -------

        tableau: a numpy array
    """
    return np.append(np.roll(tableau[:,:-1], shape[0], axis=1),
                     np.ones((shape[0], 1)), axis=1)

def tableau_to_strategy(tableau, basic_labels, strategy_labels):
    """
    Return a strategy vector from a tableau

    Parameters
    ----------

        tableau: a numpy array
        basic_labels: a set
        strategy_labels: a set

    Returns
    -------

        strategy: a numpy array
    """
    #print("bl", basic_labels)
    #print("sl",strategy_labels)
    vertex = []
    for column in strategy_labels:
        if column in basic_labels:
            for i, row in enumerate(tableau[:, column]):
                if row != 0:
                    vertex.append(tableau[i, -1] / row)
                    #print("v", vertex)
        else:
            vertex.append(0)
    strategy = np.array(vertex)
    #print("v",vertex)
    #print("str",strategy)
    #print("str_nor",strategy/sum(strategy))
    return strategy / sum(strategy)

def update_graph(r,c,steps):
    if steps == 1:
        plt.ion()
        plt.show()

    #fig, ax1, ax2 = plt.subplots(nrows=1,ncols=2)
    f, (ax1, ax2) = plt.subplots(1, 2, sharex='col', sharey='row')
    print(len(r))
    print(len(c))
    N1 = len(r)
    N2 = len(c)

    #x = range(N)
    x1 = range(1, len(r) + 1 ,1) #
    x2 = range(1, len(c) + 1, 1)  #

    width = 1
    ax1.bar(x1, r, width, color="blue")
    ax2.bar(x2, c, width, color="red")
    ax1.set_ylim([0, 1])
    ax2.set_ylim([0, 1])
    ind1 = np.arange(N1)  # the x locations for the groups
    ind2 = np.arange(N2)  # the x locations for the groups

    ax1.set_xticks(ind1 + width)
    ax2.set_xticks(ind2 + width)
    xs1 = []
    xs2 = []
    for i in range(N1):
        xs1.append('A' + str(i + 1))
    for i in range(N2):
        xs2.append('B' + str(i + 1))

    ax1.set_xticklabels(xs1)
    ax2.set_xticklabels(xs2)

    fig = plt.gcf()
    plt.title("Steps:" + str(steps))
    plt.draw()
    plt.pause(1)

def lemke_howson(A, B, initial_dropped_label=0):
    """
    Obtain the Nash equilibria using the Lemke Howson algorithm implemented
    using integer pivoting.

    Algorithm implemented here is Algorithm 3.6 of [Nisan2007]_.

    1. Start at the artificial equilibrium (which is fully labeled)
    2. Choose an initial label to drop and move in the polytope for which
       the vertex has that label to the edge
       that does not share that label. (This is implemented using integer
       pivoting)
    3. A label will now be duplicated in the other polytope, drop it in a
       similar way.
    4. Repeat steps 2 and 3 until have Nash Equilibrium.

    Parameters
    ----------

        initial_dropped_label: int

    Returns
    -------

        equilibria: A tuple.
    """

    if np.min(A) <= 0:
        A = A + abs(np.min(A)) + 1
    if np.min(B) <= 0:
        B = B + abs(np.min(B)) + 1
    
    # build tableaux
    col_tableau = make_tableau(A)
    col_tableau = shift_tableau(col_tableau, A.shape)
    row_tableau = make_tableau(B.transpose())
    full_labels = set(range(sum(A.shape)))

    if initial_dropped_label in non_basic_variables(row_tableau):
        tableux = cycle((row_tableau, col_tableau))
    else:
        tableux = cycle((col_tableau, row_tableau))

    count = 0
    # First pivot (to drop a label)
    entering_label = pivot_tableau(next(tableux), initial_dropped_label)
    #print("shape_tab", np.shape(tableux))


    row_strategies = []
    col_strategies = []
    r2 = tableau_to_strategy(row_tableau, non_basic_variables(col_tableau),
                            range(A.shape[0]))

    c2 = tableau_to_strategy(col_tableau, non_basic_variables(row_tableau),
                            range(A.shape[0], sum(A.shape)))

    #print("r: ", r2)
    #print("c: ", c2)

    r = tableau_to_strategy(row_tableau, non_basic_variables(col_tableau),
                            range(A.shape[0]))

    c = tableau_to_strategy(col_tableau, non_basic_variables(row_tableau),
                            range(A.shape[0], sum(A.shape)))

    #print("r: ", r)
    #print("c: ", c)
    # The flag of visualaztion step by step.
    flag_visualize = True

    if flag_visualize == True:
        if np.shape(r2)[0] == A.shape[0]:
            row_strategies.append(r2)
        if np.shape(c2)[0] == A.shape[1]:
            col_strategies.append(c2)
        tmp_r = np.zeros(shape=A.shape[0])
        tmp_c = np.zeros(shape=A.shape[1])

    while non_basic_variables(row_tableau).union(non_basic_variables(col_tableau)) != full_labels:
        count = count + 1
        
        entering_label = pivot_tableau(next(tableux), next(iter(entering_label)))
        #print("entering label", entering_label)

        r = tableau_to_strategy(row_tableau, non_basic_variables(col_tableau),
                                           range(A.shape[0]))

        c = tableau_to_strategy(col_tableau, non_basic_variables(row_tableau),
                                           range(A.shape[0], sum(A.shape)))

        if flag_visualize == True:
            if np.shape(r)[0] == A.shape[0]:
                row_strategies.append(r)
                update_graph(r, tmp_c, count)
                tmp_r = r
            if np.shape(c)[0] == A.shape[1]:
                col_strategies.append(c)
                update_graph(tmp_r, c, count)
                tmp_c = c
            #print("r: ", r)
            #print("c: ", c)

    #print("count:",count)

    row_strategy = tableau_to_strategy(row_tableau, non_basic_variables(col_tableau),
                                       range(A.shape[0]))


    col_strategy = tableau_to_strategy(col_tableau, non_basic_variables(row_tableau),
                                       range(A.shape[0], sum(A.shape)))


    if row_strategy.shape != (A.shape[0],) and col_strategy.shape != (A.shape[0],):
        msg = """The Lemke Howson algorithm has returned probability vectors of 
incorrect shapes. This indicates an error. Your game could be degenerate."""

        warnings.warn(msg, RuntimeWarning)
    return row_strategy, col_strategy, count
