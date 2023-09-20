import math
import itertools

from bisect import insort

from graph import Graph, same_path
from graph.random import random_xy_graph
from tests import test_graph


def lec_24_graph():
    """Sample from https://www.youtube.com/watch?v=-cLsEHP0qt0

    Lecture series on Advanced Operations Research by
    Prof. G.Srinivasan, Department of Management Studies, IIT Madras.
    For more details on NPTEL visit http://nptel.iitm.ac.in

    """
    return Graph(
        from_list=[
            (1, 2, 10),
            (1, 3, 8),
            (1, 4, 9),
            (1, 5, 7),
            (2, 1, 10),
            (2, 3, 10),
            (2, 4, 5),
            (2, 5, 6),
            (3, 1, 8),
            (3, 2, 10),
            (3, 4, 8),
            (3, 5, 9),
            (4, 1, 9),
            (4, 2, 5),
            (4, 3, 8),
            (4, 5, 6),
            (5, 1, 7),
            (5, 2, 6),
            (5, 3, 9),
            (5, 4, 6),
        ]
    )


def lec_24_brute_force():
    """Generates all combinations of solutions"""
    g = lec_24_graph()
    L = []
    shortest_tour = float("inf")
    for tour in itertools.permutations(g.nodes(), len(g.nodes())):
        d = g.distance_from_path(tour + (tour[0],))
        if d <= shortest_tour:
            insort(L, (d, tour))  # solutions are inserted by ascending distance.
            shortest_tour = d

    solutions = set()
    p1 = L[0][1]  # first solution == shortest tour.
    for d, t in L:
        if d == shortest_tour:
            t_reverse = tuple(list(t)[::-1])
            if any(
                [
                    g.same_path(t, p1),  # same path just offset in sequence.
                    g.same_path(t_reverse, p1),
                ]  # same path reversed.
            ):
                solutions.add(t)
            else:
                raise AssertionError
    return solutions


lec_24_tsp_path = [1, 3, 4, 2, 5]
lec_24_valid_solutions = lec_24_brute_force()
assert tuple(lec_24_tsp_path) in lec_24_valid_solutions


def test_greedy():
    g = lec_24_graph()
    d, tour = g.solve_tsp(method="greedy")
    assert tuple(tour) in lec_24_valid_solutions
    assert g.same_path(tour, lec_24_tsp_path)


def test_branch_and_bound():
    g = lec_24_graph()
    d, tour = g.solve_tsp(method="bnb")
    assert d == 34
    assert tuple(tour) in lec_24_valid_solutions


def test_bnb():
    g = Graph(
        from_list=[
            ((755, 53), (282, 126), 478.60004178854814),
            ((755, 53), (559, 45), 196.16319736382766),
            ((755, 53), (693, 380), 332.8257802514703),
            ((755, 53), (26, 380), 798.9806005154318),
            ((755, 53), (229, 72), 526.3430440311718),
            ((755, 53), (655, 58), 100.12492197250393),
            ((282, 126), (559, 45), 288.60006930006097),
            ((282, 126), (655, 58), 379.14772846477666),
            ((282, 126), (229, 72), 75.66372975210778),
            ((282, 126), (755, 53), 478.60004178854814),
            ((282, 126), (26, 380), 360.6272313622475),
            ((282, 126), (693, 380), 483.15318481823135),
            ((655, 58), (559, 45), 96.87620966986684),
            ((655, 58), (26, 380), 706.6293229126569),
            ((655, 58), (693, 380), 324.2344830520036),
            ((655, 58), (755, 53), 100.12492197250393),
            ((655, 58), (282, 126), 379.14772846477666),
            ((655, 58), (229, 72), 426.2299848673249),
            ((559, 45), (26, 380), 629.5347488423495),
            ((559, 45), (655, 58), 96.87620966986684),
            ((559, 45), (693, 380), 360.8060420780118),
            ((559, 45), (755, 53), 196.16319736382766),
            ((559, 45), (229, 72), 331.1027030998086),
            ((559, 45), (282, 126), 288.60006930006097),
            ((26, 380), (229, 72), 368.8807395351511),
            ((26, 380), (693, 380), 667.0),
            ((26, 380), (655, 58), 706.6293229126569),
            ((26, 380), (282, 126), 360.6272313622475),
            ((26, 380), (755, 53), 798.9806005154318),
            ((26, 380), (559, 45), 629.5347488423495),
            ((229, 72), (693, 380), 556.9201019895044),
            ((229, 72), (755, 53), 526.3430440311718),
            ((229, 72), (655, 58), 426.2299848673249),
            ((229, 72), (559, 45), 331.1027030998086),
            ((229, 72), (26, 380), 368.8807395351511),
            ((229, 72), (282, 126), 75.66372975210778),
            ((693, 380), (755, 53), 332.8257802514703),
            ((693, 380), (229, 72), 556.9201019895044),
            ((693, 380), (282, 126), 483.15318481823135),
            ((693, 380), (26, 380), 667.0),
            ((693, 380), (559, 45), 360.8060420780118),
            ((693, 380), (655, 58), 324.2344830520036),
        ]
    )
    d1, tour1 = g.solve_tsp("bnb")
    d2, tour2 = g.solve_tsp("greedy")
    assert d1 == d2


def simplify(graph):
    """helper that simplifies the xy to mere node ids."""
    d = {}
    cnt = itertools.count(1)
    c2 = []
    for s, e, dst in graph.edges():
        if s not in d:
            d[s] = next(cnt)
        if e not in d:
            d[e] = next(cnt)
        c2.append((d[s], d[e], dst))

    g = Graph(from_list=c2)
    return g


def test_random_graph_3_bnb():
    from random import seed, randint

    for i in range(4, 12):
        s = randint(1, int(1e7))
        seed(s)
        g = random_xy_graph(i, x_max=800, y_max=400)  # a fully connected graph.
        g = simplify(g)
        d1, t1 = g.solve_tsp("bnb")
        d2, t2 = g.solve_tsp("greedy")
        assert d1 <= d2 or math.isclose(d1, d2), (d1, d2, g.edges())
        print(i, s, "|", round(100 * ((d2 - d1) / d1)), "% greedy dist excess rel to bnb dist")


def test_random_graph_4_bnb():
    # fmt:off
    c = [(1, 2, 467.8226159560908), (1, 3, 561.6021723604708), (1, 4, 138.88484438555562), (1, 5, 661.6358515074587), (1, 6, 654.3951405687545), (1, 7, 114.82595525402782), (1, 8, 276.99097458220547), (1, 9, 519.7172308092161), (1, 10, 186.52613757862463), (1, 11, 205.08047201037937), (2, 3, 96.87620966986684), (2, 10, 288.60006930006097), (2, 6, 360.8060420780118), (2, 1, 467.8226159560908), (2, 11, 384.9623358200124), (2, 4, 331.1027030998086), (2, 7, 526.7988230814492), (2, 8, 629.5347488423495), (2, 5, 196.16319736382766), (2, 9, 178.04493814764857), (3, 4, 426.2299848673249), (3, 8, 706.6293229126569), (3, 6, 324.2344830520036), (3, 11, 462.0140690498505), (3, 9, 166.67633305301626), (3, 7, 623.4163937530036), (3, 5, 100.12492197250393), (3, 10, 379.14772846477666), (3, 1, 561.6021723604708), (3, 2, 96.87620966986684), (4, 8, 368.8807395351511), (4, 10, 75.66372975210778), (4, 11, 187.2671887971836), (4, 6, 556.9201019895044), (4, 5, 526.3430440311718), (4, 3, 426.2299848673249), (4, 1, 138.88484438555562), (4, 7, 203.8430768998545), (4, 9, 402.9900743194552), (4, 2, 331.1027030998086), (5, 2, 196.16319736382766), (5, 10, 478.60004178854814), (5, 1, 661.6358515074587), (5, 8, 798.9806005154318), (5, 11, 555.6005759536251), (5, 4, 526.3430440311718), (5, 3, 100.12492197250393), (5, 7, 722.9474393066207), (5, 9, 222.25210910135362), (5, 6, 332.8257802514703), (6, 3, 324.2344830520036), (6, 7, 753.7214339528895), (6, 5, 332.8257802514703), (6, 8, 667.0), (6, 10, 483.15318481823135), (6, 2, 360.8060420780118), (6, 4, 556.9201019895044), (6, 1, 654.3951405687545), (6, 9, 185.23768515072737), (6, 11, 469.847847712427), (7, 3, 623.4163937530036), (7, 8, 364.0673014704836), (7, 6, 753.7214339528895), (7, 9, 606.2878854141818), (7, 4, 203.8430768998545), (7, 1, 114.82595525402782), (7, 10, 272.21498856602295), (7, 2, 526.7988230814492), (7, 5, 722.9474393066207), (7, 11, 318.56710439089596), (8, 6, 667.0), (8, 5, 798.9806005154318), (8, 2, 629.5347488423495), (8, 4, 368.8807395351511), (8, 10, 360.6272313622475), (8, 3, 706.6293229126569), (8, 11, 244.9693858423946), (8, 7, 364.0673014704836), (8, 1, 276.99097458220547), (8, 9, 601.5064421932653), (9, 11, 368.40195439221003), (9, 1, 519.7172308092161), (9, 6, 185.23768515072737), (9, 7, 606.2878854141818), (9, 2, 178.04493814764857), (9, 8, 601.5064421932653), (9, 10, 335.574134879314), (9, 5, 222.25210910135362), (9, 3, 166.67633305301626), (9, 4, 402.9900743194552), (10, 6, 483.15318481823135), (10, 3, 379.14772846477666), (10, 4, 75.66372975210778), (10, 5, 478.60004178854814), (10, 1, 186.52613757862463), (10, 8, 360.6272313622475), (10, 9, 335.574134879314), (10, 11, 139.77839604173457), (10, 7, 272.21498856602295), (10, 2, 288.60006930006097), (11, 4, 187.2671887971836), (11, 1, 205.08047201037937), (11, 8, 244.9693858423946), (11, 10, 139.77839604173457), (11, 9, 368.40195439221003), (11, 7, 318.56710439089596), (11, 5, 555.6005759536251), (11, 6, 469.847847712427), (11, 2, 384.9623358200124), (11, 3, 462.0140690498505)]
    # fmt:on
    g = Graph(from_list=c)
    d1, t1 = g.solve_tsp("bnb")
    d2, t2 = g.solve_tsp("greedy")
    assert d1 <= d2 or math.isclose(d1, d2), (d1, d2, g.edges())
    print(round(100 * ((d2 - d1) / d1)), "% greedy dist / bnb dist")


def test_cyclic_condition():
    """
    Below is a fully connected graph for this setup

    Lane 9 <--- locations: 60 & 70  <--- Lane 9 end
    ^                                        ^
    |                                        |
    v                                        v
    Lane 10 ---> locations: 20...70 ---> Lane 10 end
    ^                                        ^
    |                                        |
    v                                        v
    Lane 11 <--- locations 20...50 <--- Lane 11 end
    """

    # fmt:off
    g = Graph(
        from_dict={
            "10,20": {"10,20":  0, "10,30":  1, "10,40":  2, "10,50":  3, "11,30": 14, "18,30": 27, "11,50": 12, "11,40": 13, "11,20": 15, "10,60":  4, "10,70":  5, "9,70": 10, "9,60": 11},
            "10,30": {"10,20": 19, "10,30":  0, "10,40":  1, "10,50":  2, "11,30": 13, "18,30": 26, "11,50": 11, "11,40": 12, "11,20": 14, "10,60":  3, "10,70":  4, "9,70":  9, "9,60": 10},
            "10,40": {"10,20": 18, "10,30": 19, "10,40":  0, "10,50":  1, "11,30": 12, "18,30": 25, "11,50": 10, "11,40": 11, "11,20": 13, "10,60":  2, "10,70":  3, "9,70":  8, "9,60":  9},
            "10,50": {"10,20": 17, "10,30": 18, "10,40": 19, "10,50":  0, "11,30": 11, "18,30": 24, "11,50":  9, "11,40": 10, "11,20": 12, "10,60":  1, "10,70":  2, "9,70":  7, "9,60":  8},
            "11,30": {"10,20":  6, "10,30":  7, "10,40":  8, "10,50":  9, "11,30":  0, "18,30": 13, "11,50": 18, "11,40": 19, "11,20":  1, "10,60": 10, "10,70": 11, "9,70": 16, "9,60": 17},
            "18,30": {"10,20": 25, "10,30": 26, "10,40": 27, "10,50": 28, "11,30": 19, "18,30":  0, "11,50": 17, "11,40": 18, "11,20": 20, "10,60": 29, "10,70": 30, "9,70": 17, "9,60": 18},
            "11,50": {"10,20":  8, "10,30":  9, "10,40": 10, "10,50": 11, "11,30":  2, "18,30": 15, "11,50":  0, "11,40":  1, "11,20":  3, "10,60": 12, "10,70": 13, "9,70": 18, "9,60": 19},
            "11,40": {"10,20":  7, "10,30":  8, "10,40":  9, "10,50": 10, "11,30":  1, "18,30": 14, "11,50": 19, "11,40":  0, "11,20":  2, "10,60": 11, "10,70": 12, "9,70": 17, "9,60": 18},
            "11,20": {"10,20":  5, "10,30":  6, "10,40":  7, "10,50":  8, "11,30": 19, "18,30": 12, "11,50": 17, "11,40": 18, "11,20":  0, "10,60":  9, "10,70": 10, "9,70": 15, "9,60": 16},
            "10,60": {"10,20": 16, "10,30": 17, "10,40": 18, "10,50": 19, "11,30": 10, "18,30": 23, "11,50":  8, "11,40":  9, "11,20": 11, "10,60":  0, "10,70":  1, "9,70":  6, "9,60":  7},
            "10,70": {"10,20": 15, "10,30": 16, "10,40": 17, "10,50": 18, "11,30":  9, "18,30": 22, "11,50":  7, "11,40":  8, "11,20": 10, "10,60": 19, "10,70":  0, "9,70":  5, "9,60":  6},
             "9,70": {"10,20": 10, "10,30": 11, "10,40": 12, "10,50": 13, "11,30": 24, "18,30": 19, "11,50": 22, "11,40": 23, "11,20": 25, "10,60": 14, "10,70": 15, "9,70":  0, "9,60":  1},
             "9,60": {"10,20":  9, "10,30": 10, "10,40": 11, "10,50": 12, "11,30": 23, "18,30": 18, "11,50": 21, "11,40": 22, "11,20": 24, "10,60": 13, "10,70": 14, "9,70": 19, "9,60":  0},
        }
    )
    # fmt:on
    def exhaustive(g):
        # d2, p2 = exhaustive() this takes 13 minutes to run, so here are the precomputed results:
        # fmt:off
        p2 = ("10,20", "10,30", "10,40", "10,50", "10,60", "10,70", "11,50", "11,40", "11,30", "11,20", "18,30", "9,70", "9,60")
        # fmt:on
        d2 = 54
        return d2, p2
        # The code below is here as documentation.        
        # assert isinstance(g, Graph)
        # dm = g.all_pairs_shortest_paths()
        # route = g.nodes()
        # d2 = 999999999
        # for tour in itertools.permutations(route, len(route)):
        #     if tour[0] != route[0]:  # all subsequent iterations are rotations of the first set.
        #         break
        #     tour += (tour[0],)
        #     d = sum(dm[a][b] for a,b in zip(tour[:-1], tour[1:]))
        #     if d < d2:
        #         d2 = d
        #         p2 = tour[:-1]
        # return d2,p2

    d2, p2 = exhaustive(g)
    d1, p1 = g.solve_tsp()
    """
    Running TSP before 2023 leads to the following oscillation 

                                                            V        V        V        V
    ['9,70', '9,60', '10,20', '10,30', '10,40', '10,50', '11,30', '18,30', '11,50', '11,40', '11,20', '10,60', '10,70']
    ['9,70', '9,60', '10,20', '10,30', '10,40', '10,50', '11,40', '11,30', '18,30', '11,50', '11,20', '10,60', '10,70']
    ['9,70', '9,60', '10,20', '10,30', '10,40', '10,50', '11,30', '18,30', '11,50', '11,40', '11,20', '10,60', '10,70']
    ['9,70', '9,60', '10,20', '10,30', '10,40', '10,50', '11,40', '11,30', '18,30', '11,50', '11,20', '10,60', '10,70']
    ['9,70', '9,60', '10,20', '10,30', '10,40', '10,50', '11,30', '18,30', '11,50', '11,40', '11,20', '10,60', '10,70']
    ['9,70', '9,60', '10,20', '10,30', '10,40', '10,50', '11,40', '11,30', '18,30', '11,50', '11,20', '10,60', '10,70']
    ['9,70', '9,60', '10,20', '10,30', '10,40', '10,50', '11,30', '18,30', '11,50', '11,40', '11,20', '10,60', '10,70']
    ['9,70', '9,60', '10,20', '10,30', '10,40', '10,50', '11,40', '11,30', '18,30', '11,50', '11,20', '10,60', '10,70']
    ['9,70', '9,60', '10,20', '10,30', '10,40', '10,50', '11,30', '18,30', '11,50', '11,40', '11,20', '10,60', '10,70']
    ['9,70', '9,60', '10,20', '10,30', '10,40', '10,50', '11,40', '11,30', '18,30', '11,50', '11,20', '10,60', '10,70']
    ['9,70', '9,60', '10,20', '10,30', '10,40', '10,50', '11,30', '18,30', '11,50', '11,40', '11,20', '10,60', '10,70']
    ['9,70', '9,60', '10,20', '10,30', '10,40', '10,50', '11,40', '11,30', '18,30', '11,50', '11,20', '10,60', '10,70']
    ['9,70', '9,60', '10,20', '10,30', '10,40', '10,50', '11,30', '18,30', '11,50', '11,40', '11,20', '10,60', '10,70']
    """
    assert d1 == d2
    assert g.has_path(p2)
    assert g.has_path(p1)

