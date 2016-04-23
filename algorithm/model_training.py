import numpy as np
import os
import logging
from os.path import dirname, abspath
from sklearn import svm
from sklearn import cross_validation
from sklearn.metrics import precision_score, recall_score, mean_absolute_error
from sklearn.grid_search import GridSearchCV
from sklearn.externals import joblib

def load_data(train_data, sample_size):		
	# print training.shape
	nrow = train_data.shape[0]
	ncol = train_data.shape[1]	
	rnd_rows = np.random.randint(nrow-1, size = sample_size)	

	data = train_data[rnd_rows,0:ncol-2]
	target = train_data[rnd_rows,ncol-1]

	print data.shape
	print target.shape
	print data
	print target
	return (data, target)

def evaluate():
		LOG_FILE = 'training history.log'
		logging.basicConfig(filename = LOG_FILE, level = logging.DEBUG)

		data, target = load_data()		
				
		parameters = [
			{'C': [1, 10, 100], 'kernel': ['linear']},
			{'C': [1, 10, 100], 'gamma': [0.01, 0.001, 0.0001], 'kernel': ['rbf']},
		]
				
		# cross-validation generator
		n_samples = data.shape[0]
		ss = cross_validation.ShuffleSplit(n_samples, n_iter = 5, test_size = 0.2, random_state = 0)					
		for train_index, test_index in ss:
			print("%s %s" % (train_index, test_index))
		 
		# grid search				
		logging.debug("Training models...")
		logging.debug("Sample size is = %d" % n_samples)
		estimator = svm.SVC()
		clf = GridSearchCV(estimator, parameters, verbose = 3, cv=ss, n_jobs = 4)
		clf.fit(data, target)		

		print "Best parameters set found on development set:"    
		print clf.best_params_

		logging.debug("Best parameters set found on development set:")
		logging.debug(clf.best_params_)

		print "\n"
		print "Grid scores on development set:"
		logging.debug("Grid scores on development set:")
		for params, mean_score, scores in clf.grid_scores_:
			print "%0.3f (+/-%0.03f) for %r" % (mean_score, scores.std() * 2, params)
			logging.debug("%0.3f (+/-%0.03f) for %r" % (mean_score, scores.std() * 2, params))		
		
		logging.debug("Training finished.")

		# scores = cross_validation.cross_val_score(clf, data, targets[:, label], cv = ss)				
		# print ("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))	

def train(data, sample_size):
	LOG_FILE = 'training history.log'
	logging.basicConfig(filename = LOG_FILE, level = logging.DEBUG)
	
	data, target = load_data(data, sample_size)
	X_train, X_test, y_train, y_test = cross_validation.train_test_split(data, target, test_size = 0.2, random_state = 0)		
	
	print "Training model..."
	logging.debug("Sample size = %d" % sample_size)
	clf = svm.SVC(kernel = 'linear', C = 100).fit(X_train, y_train)

	if sample_size == 50000:
		joblib.dump(clf, 'models/svr_linear_100.pkl')

	print "Predicting model..."
	y_pred = clf.predict(X_test)					
	print "Mean accuracy : %0.3f" % clf.score(X_test, y_test)
	print "Precision     : %0.3f" % precision_score(y_test, y_pred)
	print "Recall        : %0.3f" % recall_score(y_test, y_pred)
	logging.debug("Mean accuracy : %0.3f" % clf.score(X_test, y_test))
	logging.debug("Precision     : %0.3f" % precision_score(y_test, y_pred))
	logging.debug("Recall        : %0.3f" % recall_score(y_test, y_pred))
	return clf

if __name__ == '__main__':
	ROOT_DIR = dirname(dirname(abspath(__file__)))
	filepath = os.path.join(ROOT_DIR, 'dataset/rating prediction/train.csv')
	sample_sizes = [5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000]
	data = np.loadtxt(open(filepath, "rb"), delimiter = ",", skiprows = 1)

	for size in sample_sizes:
		clf = train(data, size)
	# clf = evaluate()

