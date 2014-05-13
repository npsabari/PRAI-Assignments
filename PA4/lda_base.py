from sets import Set
import random
from numpy import array
from scipy.cluster.vq import kmeans,vq
import pickle
import operator

docs = []
vocab = Set()
num_to_word, word_to_num = {}, {}
topic_assign = {}
true_doc_labels = []
topics = 5

is_pickle = False

bad_docs = Set()

#File reading
f1 = open('docs.txt', 'r')
for line in f1:
    words = line.strip().split()
    if len(words) < 2:
        bad_docs.add(int(words[0]))
        continue
    del(words[0])
    docs.append(words)
    vocab |= Set(words)
vocab = list(vocab)
print 'Vocab size', len(vocab)
f1.close()

f2 = open('truth.txt', 'r')
for line in f2:
    words = line.strip().split()
    if int(words[0]) in bad_docs: continue
    true_doc_labels.append(words[1])
f2.close()
#End of file reading

#Create number to word map
word_cnt = 0
for word in vocab:
    word_to_num[word] = word_cnt
    num_to_word[word_cnt] = word
    word_cnt += 1
assert(word_cnt == len(vocab))
#End of map creation

#Converting docs and vocab as list of integers
tmp_docs = []
for lst in docs:
    tmp_list = []
    for j in lst: tmp_list.append(word_to_num[j])
    tmp_docs.append(tmp_list)
docs = tmp_docs

tmp_vocab = []
for w in vocab:
    tmp_vocab.append(word_to_num[w])
vocab = tmp_vocab
#End of conversions
"""
ndk = []
nkw = []
nk = []

# __init__ of matrices
ndk = [[0]* topics for id in docs]
#nkw = {w: [0]*topics for w in vocab}
nkw = [{w: 0 for w in vocab} for it in xrange(topics)]
nk = [0]*topics
for id, lst in enumerate(docs):
    tmp_list= []
    for j in lst:
        tmp = random.randint(0, topics-1)
        tmp_list.append(tmp)
        ndk[id][tmp] += 1
        nkw[tmp][j] += 1
        nk[tmp] += 1
    topic_assign[id] = tmp_list
#End of init

if not is_pickle:
    #Perform LDA with Gibbs sampling
    alpha = 50/float(topics)
    beta = 0.01
    max_iter = 100
    for i_iter in xrange(max_iter):
        print 'iterations done', i_iter
        for id, lst in enumerate(docs):
            for it, t in enumerate(lst):
                it_topic = topic_assign[id][it]
                ndk[id][it_topic] -= 1
                nkw[it_topic][t] -= 1
                nk[it_topic] -= 1
                dist = [(ndk[id][ik]+alpha)*(nkw[ik][t]+beta)/float(nk[ik]+beta*len(vocab)) for ik in xrange(topics)]
                prob_dist = [i_val/sum(dist) for i_val in dist]

                #Sample for prob_dist
                cumsum = 0
                tmp_rand = random.random()
                for ik, val in enumerate(prob_dist):
                    cumsum += val
                    if tmp_rand <= cumsum:
                        it_topic = ik
                        break
                #End of sampling

                topic_assign[id][it] = it_topic
                ndk[id][it_topic] += 1
                nkw[it_topic][t] += 1
                nk[it_topic] += 1
        #print nk
    #End of LDA/Gibbs
"""
#Baseline
ndk = []
for it, lst in enumerate(docs):
    tmp_lst = []
    for w in vocab:
        j = lst.count(w)
        if j > 0: tmp_lst.append(1)
        else: tmp_lst.append(0)
    ndk.append(tmp_lst)
#End

#Normalize ndk matrix for KMeans
tmp_ndk = []
for w in ndk:
    tmp_sum = float(sum(w))
    tmp_ndk.append([it/tmp_sum for it in w])
ndk = tmp_ndk
#End of Normalization

"""
f3 = open('topic_word_lst.txt', 'w')
for it, t in enumerate(nkw):
    f3.write('Topic '+str(it)+': ')
    sorted_x = sorted(t.iteritems(), key=operator.itemgetter(1))
    sorted_x.reverse()
    for i in xrange(20):
        f3.write(num_to_word[sorted_x[i][0]]+'-'+str(sorted_x[i][1])+', ')
    f3.write('\n')
f3.close()
#Normalize nkw matrix for word distribution
tmp_nkw = []
for it in nkw:
    tmp_sum = float(sum(it.values()))
    tmp_nkw.append({ik: cnt/tmp_sum for ik, cnt in it.iteritems()})
nkw = tmp_nkw
#End of Normalization

f3 = open('word_distribution.txt', 'w')
for word in vocab:
    f3.write(num_to_word[word]+' ')
f3.write('\n')
for it, lst in enumerate(nkw):
    f3.write('Topic '+str(it)+' ')
    for word in vocab:
        f3.write(str(lst[word])+' ')
    f3.write('\n')
f3.close()
"""

#Dump for future use
#pickle.dump(ndk, open("100_"+str(topics)+"_ndk.p", "wb"))
#pickle.dump(nkw, open("100_"+str(topics)+"_nkw.p", "wb"))
#End of dump
num_clus = [i for i in xrange(5, 6)]
for num_clusters in num_clus:
#Perform clustering
    centroids,_ = kmeans(array(ndk), num_clusters)
    doc_labls,_ = vq(array(ndk), centroids)
    #End of clustering

    topic_counts = {i: dict() for i in xrange(num_clusters)}
    for i, i_val in enumerate(doc_labls):
        lab = true_doc_labels[i]
        if topic_counts[i_val].has_key(lab):
            topic_counts[i_val][lab] += 1
        else:
            topic_counts[i_val][lab] = 1
    num_cnt = 0
    for it, cnts in topic_counts.iteritems():
        try:
            num_cnt += cnts[max(cnts, key=cnts.get)]
        except ValueError:
            pass
    purity = float(num_cnt)/float(len(docs))
    print num_clusters, " Clusters - Purity ", purity
