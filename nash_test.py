import nash
import numpy as np
import datetime
import matplotlib.pyplot as plt

# Algorithms
def non_duplicate_print(eqs):
    tmp1 = []
    tmp2 = []
    for eq in eqs:
        #print("eq:",eq,"tmp:",tmp)
        #print(np.any(eq in tmp))
        #print(eq in tmp)
        # print(tmp1,tmp2)
        if len(tmp1) == 0 and len(tmp2) == 0:
            tmp1.append(eq[0])
            tmp2.append(eq[1])
            print(eq)
            flag = False
        for i in range(len(tmp1)):
            if np.all(eq[0] == tmp1[i]):
                if np.all(eq[1] == tmp2[i]):
                    flag = True
        if flag is False:
            tmp1.append(eq[0])
            tmp2.append(eq[1])
            print(eq)

def find_nash_support_enum(utilA , utilB):
    random_game = nash.Game(utilA, utilB)
    eqs = random_game.support_enumeration()
    non_duplicate_print(eqs)
def find_nash_lemke_howson(utilA , utilB):
    random_game = nash.Game(utilA, utilB)
    random_game.lemke_howson(initial_dropped_label=0)
    eqs = random_game.lemke_howson_enumeration()
    non_duplicate_print(eqs)
def find_nash_vertex_enum(utilA , utilB):
    random_game = nash.Game(utilA, utilB)
    for eq in random_game.vertex_enumeration():
        print(eq)
# generate m x n 2-player game
def generate_game(m = 2, n = 2, utility_max = 10, utility_min = -10):
    # two player game, multiple actions (m x n)
    # m = 6
    # n = 4
    # utility_max = 10
    # utility_min = -10
    print("Rows:", m, "Cols:", n, "Max:", utility_max, "Min:", utility_min)

    utilA = np.random.random_integers(utility_min, utility_max, size=(m, n))
    utilB = np.random.random_integers(utility_min, utility_max, size=(m, n))
    utilA = np.asarray(utilA, dtype=np.int8)
    utilB = np.asarray(utilB, dtype=np.int8)

    print("utility of row player")
    print(utilA)
    print("utility of col player")
    print(utilB)
    return utilA, utilB

# generate a single m x n game
def gen_single_game(m, n):
    a, b = generate_game(m=m, n=n)
    t1 = datetime.datetime.now()
    print("Support Enumeration")
    find_nash_support_enum(a, b)
    print("Lemke Howson")
    find_nash_lemke_howson(a, b)
    print("Vertex Enumeration")
    find_nash_vertex_enum(a, b)
    t2 = datetime.datetime.now()
    diff = t1 - t2
    tdiff_sec = abs(diff.total_seconds())
    print("Time cost for finding NE:", tdiff_sec)

def plot_cal_time(arrs):

    # debug
    print(arrs[0])
    print(arrs[1])
    print(arrs[2])

    #
    len1 = len(arrs[0])
    x = range(2, len1+2)
    plt.title('Finding NE in a symmetric game')
    plt.xlabel('The number of actions')
    plt.ylabel('Running Time in second')
    #plt.xlim(xmin=2)
    a0, = plt.plot(x, arrs[0], 'r')
    a1, = plt.plot(x, arrs[1], 'g')
    a2, = plt.plot(x, arrs[2], 'b')
    plt.legend((a0, a1, a2), ('Support Enum','LH','Vertex Enum'))
    plt.show()

def gen_multi_games(m, n):
    max1 = max(m, n)
    len_algorithms = 3
    arr_tdiffs = []
    # Loop all algorithm
    for ind in range(len_algorithms):
        arr_tdiff = []
        for i in range(2, max1+1, 1):
            a, b = generate_game(m=i, n=i)
            # time start for the various algorithms
            t1 = datetime.datetime.now()
            # pick up one algorithm
            if ind == 0:
                find_nash_support_enum(a, b)
            elif ind == 1:
                find_nash_lemke_howson(a, b)
            elif ind == 2:
                find_nash_vertex_enum(a, b)
            t2 = datetime.datetime.now()
            # time end
            diff = t1 - t2
            tdiff_sec = abs(diff.total_seconds())
            arr_tdiff.append(tdiff_sec)
            print("Time cost for finding NE:", tdiff_sec)
        arr_tdiffs.append(arr_tdiff)
    # plotting
    plot_cal_time(arr_tdiffs)


# main -> find_nash -> random_game.support_enumeration()
# loop symmetric games from (2,2) to (10,10) actions
#gen_multi_games(12, 12)
# single game test
gen_single_game(3, 3)








