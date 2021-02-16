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
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

colored_markers = [marker + color for marker, color in itertools.product(colors, markers)]
shuffle(colored_markers)

cm_ind = 0


def find_centroid(cluster):
    global points_list

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


def euclidean_distance(cluster_a, cluster_b):
    global points_list

    sum_squared = 0

    if len(cluster_a) == 1:
        centroid_a = points_list[cluster_a[0]]
    else:
        centroid_a = find_centroid(cluster_a)

    if len(cluster_b) == 1:
        centroid_b = points_list[cluster_b[0]]
    else:
        centroid_b = find_centroid(cluster_b)

    for i in range(0, dimensions):
        x = centroid_a[i]
        y = centroid_b[i]

        sum_squared += pow((x - y), 2)
    euclidean_dist = math.sqrt(sum_squared)

    return euclidean_dist


def find_new_cluster_pairwise_distance(start_ind, heap):
    cluster_a = index_list[start_ind]
    for ind in range(start_ind + 1, len(index_list)):
        cluster_b = index_list[ind]
        dist = euclidean_distance(cluster_a, cluster_b)
        dist_list = [dist, [cluster_a, cluster_b]]
        heapq.heappush(heap, dist_list)


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


def print_result(clusters, desired_clusters_amount):
    k_clusters = clusters[desired_clusters_amount]
    for k_cluster in k_clusters:
        if dimensions == 2:
            draw_cluster(k_cluster)
        else:
            print(k_cluster)

    if dimensions == 2:
        if desired_clusters_amount > len(colored_markers):
            print("It's not possible to draw so many different clusters")
        else:
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.title('Hierarchical clustering')
            plt.show()


def main():
    global dimensions, points_list, index_list
    dimensions = 0
    points_list = []
    index_list = []
    n = 0

    points = generate_input()
    desired_clusters_amount = int(sys.argv[1])

    for point in points:
        points_list.append(point)
        index_list.append([n])
        n += 1

    dimensions = len(points_list[0])
    heap = setup_input(n)
    clusters_dict = clustering(heap, n)
    print_result(clusters_dict, desired_clusters_amount)


def generate_input():
    input_list = []
    for _ in range(888):
        x = random.randint(0, 100) / 100
        y = random.randint(0, 100) / 100
        input_list.append([x, y])

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
    main()
