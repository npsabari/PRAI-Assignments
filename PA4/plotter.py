import random
import pylab as pl
import numpy as np
from sklearn import svm, datasets
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import auc

precision1 = [0.492, 0.617, 0.591, 0.618, 0.673, 0.705, 0.687, 0.751, 0.794]

recall1 = [i for i in xrange(2, 11)]

pl.clf()
pl.plot(recall1, precision1, label='Purity curve')
pl.xlabel('Number of Topics')
pl.ylabel('Purity')
pl.ylim([0.4, 0.80])
pl.xlim([2, 11])
pl.title('Purity Vs Number of Topics')
pl.legend(loc="lower left")
pl.show()
