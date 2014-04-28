from sets import Set
import random
from scipy.cluster.vq import *
import numpy
from numpy.random import multinomial
from sklearn.cluster import KMeans
import pickle

#dict: key = Doc ID ; value = list of words
docs = list()
final_doc_repr = list()

doc_labels = list()
true_doc_labels = list()

unique_words = Set()

topic_assignments = list()

ndk = list()
nkw = dict()
nk = list()

num_clusters = 6
topics = 5

def read_input():
    global docs, unique_words
    f1 = open('docs.txt', 'r')
    for line in f1:
        words = line.strip().split()
        del(words[0])
        docs.append(words)
        unique_words |= Set(words)
    unique_words = list(unique_words)
    f1.close()

def get_true_doc_topics():
    global true_doc_labels
    f2 = open('truth.txt', 'r')
    for line in f2:
        words = line.strip().split()
        true_doc_labels.append(words[1])
    f2.close()

def init_counters():
    global topic_assignments, ndk, nkw, nk, topics, docs, unique_words

    for i, v in enumerate(docs):
        topic_assignments.append(dict())
        for j in v:
            topic_assignments[i][j] = random.randint(0, topics-1)

    ndk = [[0 for i in range(topics)] for j in docs]
    nkw = {j: [0 for i in range(topics)] for j in unique_words}
    nk = [0 for i in range(topics)]
    for i, v in enumerate(docs):
        for j in v:
            ndk[i][topic_assignments[i][j]] += 1
            nkw[j][topic_assignments[i][j]] += 1
            nk[topic_assignments[i][j]] += 1

def run_lda():
    global docs, topic_assignments, topics, ndk, nkw, nk
    alpha_hyper = 50/float(topics)
    beta_hyper = 0.01
    max_iter = 10
    while max_iter > 0:
        print 'iterations left ', max_iter
        for id, d in enumerate(docs):
            for iw, w in enumerate(d):
                iw_topic = topic_assignments[id][w]
                ndk[id][iw_topic] -= 1
                nkw[w][iw_topic] -= 1
                nk[iw_topic] -= 1
                prob_dist = [0 for i in range(topics)]
                for ik in range(topics):
                    prob_dist[ik] = (ndk[id][ik]+alpha_hyper)*(nkw[w][ik]+beta_hyper)/float(nk[ik]+beta_hyper*len(unique_words))
                prob_sum = float(sum(prob_dist))
                #Normalize the sample distribution
                for i in range(topics):
                    prob_dist[i] /= prob_sum
                iw_topic = numpy.argmax(multinomial(1, prob_dist))
                topic_assignments[id][w] = iw_topic
                ndk[id][iw_topic] += 1
                nkw[w][iw_topic] += 1
                nk[iw_topic] += 1
        max_iter -= 1

def gen_doc_repr():
    global docs, topics, final_doc_repr, topic_assignments
    final_doc_repr = [[0 for i in range(topics)] for j in docs]
    for i, v in enumerate(docs):
        for j in v:
            final_doc_repr[i][topic_assignments[i][j]] += 1
        tmp_sum = float(sum(final_doc_repr[i]))
        try:
            for j in range(topics):
                final_doc_repr[i][j] /= tmp_sum
        except ZeroDivisionError:
            for j in range(topics):
                final_doc_repr[i][j] = 1.0/(topics)
    pickle.dump(final_doc_repr, open("10_5_5.p", "wb"))

def load_saved_data():
    global final_doc_repr
    final_doc_repr = pickle.load(open("1000_5_5.p", "rb"))

def run_kmeans():
    global final_doc_repr, doc_labels, num_clusters, topics
    kmeans_obj = KMeans(n_clusters = num_clusters, tol = 0.0000001)
    kmeans_obj.fit(final_doc_repr)
    doc_labels = kmeans_obj.labels_

def get_purity():
    global doc_labels, true_doc_labels, docs, num_clusters
    docs_topics = [[] for i in range(num_clusters)]
    for id, l in enumerate(doc_labels):
        docs_topics[l].append(id)

    num_correct = 0
    for _docs in docs_topics:
        topics_count = dict()
        for id in _docs:
            true_label = true_doc_labels[id]
            if topics_count.has_key(true_label): topics_count[true_label] += 1
            else: topics_count[true_label] = 1
        print topics_count
        try:
            freq_topic = max(topics_count, key=topics_count.get)
            num_correct += topics_count[freq_topic]
            print num_correct
        except:
            pass
    return num_correct/float(len(docs))

def main():
    read_input()
    get_true_doc_topics()
    #init_counters()
    #run_lda()
    #gen_doc_repr()
    load_saved_data()
    run_kmeans()
    print get_purity()

if __name__ == '__main__':
    main()
