import FeatureExtraction
import sklearn.mixture
import numpy
from os import path
import pickle

def generateModel(audioNumber, nomefile):
    results = numpy.asmatrix(())
    for i in range (1,audioNumber+1):
        originalPath = path.join(path.dirname(path.realpath(__file__)), "./mfcc/")
        mfcc = numpy.loadtxt(fname = originalPath+"mfcc"+nomefile+str(i)+".txt")
        i += 1

        if i==2:
            results = mfcc
        else:
            results = numpy.vstack((results, mfcc))

    model = sklearn.mixture.GaussianMixture(n_components = audioNumber+1, covariance_type='diag',n_init = 3)
    model.fit(results)
    #Estimate model parameters with the EM algorithm. expectation maximization


    filename = './models/model'+nomefile+".gmm"
    pickle.dump(model, open(filename, 'wb'))

#generateModel(3,"lillo")
#generateModel(3,"italian")
#generateModel(2,"amedeo")
#generateModel(2,"colucci")
#generateModel(2,"pepe")
#generateModel(2,"mamma")
#generateModel(2,"papa")
#print("fatto")