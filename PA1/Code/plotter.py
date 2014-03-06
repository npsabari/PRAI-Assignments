import random
import pylab as pl
import numpy as np
from sklearn import svm, datasets
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import auc

precision_list = list()
recall_list = list()
precision= [0.95, 0.954, 0.956, 0.960, 0.966, 0.969, 0.970, 0.9712, 0.9713, 0.9713, 0.9713, 0.9713, 0.9713, 0.9713]
recall = [0.979, 0.979, 0.979, 0.945, 0.8948, 0.831, 0.739, 0.65, 0.581, 0.524, 0.477, 0.437, 0.403, 0.374]

area = auc(recall, precision)
print("Area Under Curve: %0.2f" % area)

pl.clf()
pl.plot(recall, precision, label='Precision-Recall curve')
pl.xlabel('Recall')
pl.ylabel('Precision')
pl.ylim([0.0, 1.05])
pl.xlim([0.0, 1.0])
pl.title('Precision-Recall example: AUC=%0.2f' % area)
pl.legend(loc="lower left")
pl.show()
