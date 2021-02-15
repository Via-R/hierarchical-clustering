import sys
import heapq
import math
from random import shuffle
import random
import matplotlib.pyplot as plt
import itertools

dimensions = 0
points_list = []
index_list = []

markers = ['.', ',', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', '8', 's', 'p', 'P', '*', 'h', 'H', '+', 'x', 'X', 'D',
           'd']
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

colored_markers = [marker + color for marker, color in itertools.product(colors, markers)]
shuffle(colored_markers)

cm_ind = 0

def find_centroid(cluster, points_list):
    centroid = []
    cluster_length = len(cluster)
    cluster_list_for_centroid = []

    for i in range(0, dimensions):
        centroid.append(0.0)

    for i in range(0, cluster_length):
        cluster_list_for_centroid.append(points_list[cluster[i]])

    for i in range(0, dimensions):
        for j in range(0, cluster_length):
            centroid[i] += cluster_list_for_centroid[j][i]
        centroid[i] = centroid[i] / cluster_length
    return centroid


def euclidean_distance(cluster_a, cluster_b, points_list):
    sum_squared = 0

    # print cluster_a
    if len(cluster_a) == 1:
        centroid_a = points_list[cluster_a[0]]
    else:
        centroid_a = find_centroid(cluster_a, points_list)

    if len(cluster_b) == 1:
        centroid_b = points_list[cluster_b[0]]
    else:
        centroid_b = find_centroid(cluster_b, points_list)

    for i in range(0, dimensions):
        x = centroid_a[i]
        y = centroid_b[i]

        sum_squared += pow((x - y), 2)
    euclidean_dist = math.sqrt(sum_squared)

    return euclidean_dist


def find_new_cluster_pairwise_distance(i, heap):
    cluster_a = index_list[i]
    for k in range(i + 1, len(index_list)):
        cluster_b = index_list[k]
        dist = euclidean_distance(cluster_a, cluster_b, points_list)
        dist_list = [dist, [cluster_a, cluster_b]]
        heapq.heappush(heap, dist_list)
    # return heap


def merge_clusters(cluster_a, cluster_b):
    return sorted(list(set(cluster_a) | set(cluster_b)))


def clustering(heap, n):
    clusters_dict = {}

    while n > 1:

        closest_cluster = heapq.heappop(heap)
        cluster1 = closest_cluster[1][0]
        cluster2 = closest_cluster[1][1]

        if cluster1 in index_list and cluster2 in index_list:
            index_list.remove(cluster1)
            index_list.remove(cluster2)
            merged_cluster = merge_clusters(cluster1, cluster2)
            index_list.insert(0, merged_cluster)
            find_new_cluster_pairwise_distance(0, heap)
            n = n - 1
            clusters_dict[n] = list(index_list)

    return clusters_dict


def setup_input(n):
    heap = []
    for i in range(n - 1):
        find_new_cluster_pairwise_distance(i, heap)

    return heap


def gold_std(lines):
    gold_std_dict = {}

    index = 0
    for each in lines:
        point = each.strip().split(',')
        cluster_name = point[-1]

        gold_std_dict.setdefault(cluster_name, [])
        gold_points_list = gold_std_dict[cluster_name]
        gold_points_list.append(index)
        gold_std_dict[cluster_name] = gold_points_list
        index += 1

    return gold_std_dict


def precision_and_recall(my_pairs, gold_pairs):
    common_pairs = set(my_pairs).intersection(gold_pairs)

    my_pairs_count = float(len(my_pairs))
    gold_pairs_count = float(len(gold_pairs))
    common_pairs_count = float(len(common_pairs))

    precision = common_pairs_count / my_pairs_count
    recall = common_pairs_count / gold_pairs_count

    return precision, recall


def create_pairs(pairs, cluster):
    new_pairs = list(itertools.combinations(cluster, 2))
    pairs = pairs + new_pairs
    return pairs


def accuracy(k_clusters, lines):
    my_pairs = []
    gold_pairs = []
    for cluster in k_clusters:
        my_pairs = create_pairs(my_pairs, cluster)

    gold_std_dict = gold_std(lines)

    for key, value in gold_std_dict.items():
        gold_pairs = create_pairs(gold_pairs, value)

    precision, recall = precision_and_recall(my_pairs, gold_pairs)
    return precision, recall


def print_result(k_clusters, precision, recall):
    # print(precision)
    # print(recall)
    for k_cluster in k_clusters:
        if dimensions == 2:
            draw_cluster(k_cluster)
        # print(k_cluster)


def main(lines, k):
    global dimensions
    dimensions = 0
    global points_list
    points_list = []
    global index_list
    index_list = []
    n = 0
    for x in lines:
        data_point = [float(i) for i in x.strip().split(',')]
        points_list.append(data_point)
        index_list.append([n])
        n += 1

    dimensions = len(points_list[0])
    heap = setup_input(n)
    clusters_dict = clustering(heap, n)
    precision, recall = accuracy(clusters_dict[k], lines)
    print_result(clusters_dict[k], precision, recall)


def generate_input():
    input_list = []
    for _ in range(888):
        x = str(random.randint(0, 100) / 100)
        y = str(random.randint(0, 100) / 100)
        input_line = ",".join([x, y])
        input_list.append(input_line)

    return input_list


def draw_cluster(indexes: list):
    global cm_ind

    xs = []
    ys = []
    for i in indexes:
        xs.append(points_list[i][0])
        ys.append(points_list[i][1])

    plt.plot(xs, ys, colored_markers[cm_ind])
    cm_ind += 1


if __name__ == "__main__":
    lines = generate_input()
    k = int(sys.argv[2])
    main(lines, k)
    if dimensions == 2:
        if k > len(colored_markers):
            print("It's not possible to draw so many different clusters")
        else:
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.title('Hierarchical clustering')
            plt.show()
