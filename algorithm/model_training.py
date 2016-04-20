import numpy as np
import os
import logging
from os.path import dirname, abspath
from sklearn import svm
from sklearn import cross_validation
from sklearn.metrics import precision_score, recall_score, mean_absolute_error
from sklearn.grid_search import GridSearchCV
from sklearn.externals import joblib

def load_data():
	ROOT_DIR = dirname(dirname(abspath(__file__)))
	filepath = os.path.join(ROOT_DIR, 'dataset/rating prediction/train.csv')
	training = np.loadtxt(open(filepath, "rb"), delimiter = ",", skiprows = 1)
	
	# print training.shape
	nrow = training.shape[0]
	ncol = training.shape[1]	

	rnd_rows = np.random.randint(nrow-1, size = 10000)	

	data = training[rnd_rows,0:ncol-1]
	target = training[rnd_rows,ncol-1]

	print data.shape
	print target.shape
	print data
	print target
	return (data, target)

def train():
	data, target = load_data()
	X_train, X_test, y_train, y_test = cross_validation.train_test_split(data, target, test_size = 0.2, random_state = 0)		
	
	print "Training model..."
	clf = svm.SVR(kernel = 'linear', C = 10).fit(X_train, y_train)
	joblib.dump(clf, 'svr_linear_10.pkl')

	print "Predicting model..."
	y_pred = clf.predict(X_test)					
	print "R-square : %0.3f" % clf.score(X_test, y_test)
	print "MAE      : %0.3f" % mean_absolute_error(y_test, y_pred)
	return clf

if __name__ == '__main__':
	# load_data()
	clf = train()

