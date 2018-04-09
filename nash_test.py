import nash
import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.stats import norm

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
    a = random_game.lemke_howson(initial_dropped_label=0)
    print("NE", a[0],a[1])
    #print("row", a[3])
    #print("col", a[4])
    return a[2]
    #for eq in random_game.lemke_howson_enumeration():
    #    print(eq)
    #eqs = random_game.lemke_howson_enumeration()
    #non_duplicate_print(eqs)
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

    utilA = np.random.uniform(utility_min, utility_max, size=(m, n))
    utilB = np.random.uniform(utility_min, utility_max, size=(m, n))
    utilA = np.asarray(utilA, dtype=np.int8)
    utilB = np.asarray(utilB, dtype=np.int8)

    print("utility of row player")
    print(utilA)
    print("utility of col player")
    print(utilB)
    return utilA, utilB

# generate a single m x n game
def gen_single_game(m, n):
    # Configuration
    flag_steps_distribusion = False
    flag_single_game = True
    flag_use_customized_game = True
    flag_save_game = False

    #outfileA = 'game_A_prison.npy'
    #outfileB = 'game_B_prison.npy'
    #outfileA = 'game_A_rock.npy'
    #outfileB = 'game_B_rock.npy'
    #outfileA = 'game_A.npy'
    #outfileB = 'game_B.npy'
    outfileA = 'game_A_53.npy'
    outfileB = 'game_B_53.npy'
    # outfileA = 'game_A_12.npy'
    # outfileB = 'game_B_12.npy'





    if flag_single_game == True:
        # Generate a new game or use customized game.
        if flag_use_customized_game == True:
            a = np.load(outfileA)
            b = np.load(outfileB)
            print(a)
            print(b)
        else:
            a, b = generate_game(m=m, n=n)
            if flag_save_game == True:
                # Save
                np.save(outfileA, a)
                np.save(outfileB, b)
        a = [[3,1,5],[2,2,4]]
        b = [[2,1,0],[2,3,1]]
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

    # Cal steps distribution
    if flag_steps_distribusion == True:
        count = 0
        arrs = []
        counts = []
        for k in range(5, 9, 1):
            counts.clear()
            for i in range(300):
                a, b = generate_game(m=k, n=k)
                # Using customized game
                # a = [[0,-1,1],[1,0,-1],[-1,1,0]]
                # b = [[0,1,-1],[-1,0,1],[1,-1,0]]
                # a = [[3,0],[0,2]]
                # b = [[2,0],[0,3]]
                # Loading existing game
                # outfileA = 'game_A.npy'
                # outfileB = 'game_B.npy'
                # a = np.load(outfileA)
                # b = np.load(outfileB)
                # Run
                count = find_nash_lemke_howson(a, b)
                # Save
                # np.save(outfileA, a)
                # np.save(outfileB, b)

                print(count)
                if count <= 40:
                    counts.append(count)
            arrs.append(counts.copy())
            title = "Random size:" + str(k) + " x " + str(k)
            # plot_histogram(counts,title)
        plot_four_hist(arrs[0], arrs[1], arrs[2], arrs[3])

def plot_histogram(arrs,title):
    #x = np.random.normal(size=1000)
    #plt.hist(x, normed=True, bins=30)
    plt.ylabel('Steps to find a NE');
    plt.xlabel('counts');
    plt.title(title)
    plt.hist(arrs, bins=20)
    plt.show()
    #l = plt.plot(bins, y, 'r--', linewidth=1)
def plot_four_hist(arr1,arr2,arr3,arr4):
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row')
    (mu1, sigma1) = norm.fit(arr1)
    (mu2, sigma2) = norm.fit(arr2)
    (mu3, sigma3) = norm.fit(arr3)
    (mu4, sigma4) = norm.fit(arr4)
    mu1 = format(mu1, '.2f')
    mu2 = format(mu2, '.2f')
    mu3 = format(mu3, '.2f')
    mu4 = format(mu4, '.2f')
    sigma1 = format(sigma1, '.2f')
    sigma2 = format(sigma2, '.2f')
    sigma3 = format(sigma3, '.2f')
    sigma4 = format(sigma4, '.2f')

    ax1.hist(arr1, rwidth=0.8, color='sandybrown')
    ax2.hist(arr2, rwidth=0.8, color='sandybrown')
    ax3.hist(arr3, rwidth=0.8, color='sandybrown')
    ax4.hist(arr4, rwidth=0.8, color='sandybrown')
    plt.title("Find a NE in different Size in 300 rounds")
    ax1.set_ylabel("Counts")
    ax2.set_ylabel("Counts")
    ax3.set_ylabel("Counts")
    ax4.set_ylabel("Counts")
    str1 = "Game Size 5 x 5 " + ", u:" + str(mu1) + ", s:" + str(sigma1)
    str2 = "Game Size 6 x 6 " + ", u:" + str(mu2) + ", s:" + str(sigma2)
    str3 = "Game Size 7 x 7 " + ", u:" + str(mu3) + ", s:" + str(sigma3)
    str4 = "Game Size 8 x 8 " + ", u:" + str(mu4) + ", s:" + str(sigma4)

    ax1.set_title(str1)
    ax2.set_title(str2)
    ax3.set_title(str3)
    ax4.set_title(str4)
    plt.show()
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
    plt.tight_layout()

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
gen_single_game(5, 3)








