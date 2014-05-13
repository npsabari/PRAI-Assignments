import random
import pylab as pl
import numpy as np
from sklearn import svm, datasets
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import auc

precision = list()

f = open('./1000-results/1000_5_o.out', 'r')
for line in f:
    words = line.strip().split()
    precision.append(float(words[4]))
f.close()
recall = [i for i in xrange(2, 50)]

pl.clf()
pl.plot(recall, precision, label='Purity curve')
pl.xlabel('Number of Clusters')
pl.ylabel('Purity')
pl.ylim([0.4, 0.80])
pl.xlim([2, 50])
pl.title('Purity Vs Number of Clusters')
pl.legend(loc="lower left")
pl.show()
