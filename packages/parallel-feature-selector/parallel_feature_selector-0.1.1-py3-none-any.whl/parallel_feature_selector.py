import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from mpi4py import MPI
import csv
import sys
import os
import operator
from arff2pandas import a2p
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB, BernoulliNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import warnings
from sklearn.exceptions import DataConversionWarning
warnings.filterwarnings(action='ignore', category=DataConversionWarning, module='sklearn')
warnings.filterwarnings(action='ignore', category=UserWarning, module='openpyxl')

def bruteForce(data, estimator, testSize=0.2, randomState=42, cv=5, topScoreNo=5, shuffle=True, timeResultFile='outputTimeAnalysis.csv', scoreResultFile='outputSubsetAnalysis.csv'):
    MASTER = 0
    y = data.iloc[:, -1:]
    x = data.iloc[:, :-1]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = testSize, random_state = randomState, shuffle = shuffle)
    sc = StandardScaler()
    X_train = sc.fit_transform(x_train)
    X_test = sc.transform(x_test)

    featureNo = x_train.shape[1]
    bestScores = [0] * topScoreNo
    removedFeatureNumbers = [featureNo] * topScoreNo
    bestSubsets = [None] * topScoreNo
    intervals = None # List of subset intervals to scatter
    interval = None # Subset interval for each process

    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    startTime = MPI.Wtime() 

    if rank == MASTER:      
        length = (2**featureNo) - 1 # Total number of feature subsets
        
        while True:
            if length%size == 0:
                chunk_size = length // size # Calculate chunk size for scatter
                break
            else:
                length += 1 # If length is not completely divisible by process number, increase it by 1
                
        intervals = [[i, i+chunk_size] for i in range(1, length, chunk_size)]
        intervals[size-1][1] = (2**featureNo) # Last interval's end should be set to initial length, in case of length was modified above
        
    interval = comm.scatter(intervals, root = MASTER)

    for i in range(interval[0], interval[1]):
        subset = str(bin(i)[2:].zfill(featureNo)) # Feature mask
        featureList = []
        #print(subset)
        for j in range(featureNo):
            if subset[j] == '1':
                featureList.append(j) # Get masked features
                
        score = cross_val_score(estimator, x_train.iloc[:, list(featureList)], y_train, cv = cv).mean()
        
        if score > min(bestScores): # ms -> Abbreviation for Minimum Score
            removedFeatureNo = featureNo - len(featureList)
            msIndices = [m for m, x in enumerate(bestScores) if x == min(bestScores)]
            msRemovedFeatureNo = [removedFeatureNumbers[m] for m in msIndices]
            msMinRemovedFeatureNo = min(msRemovedFeatureNo)
            msMinIndex = None

            for m in msIndices:
                if removedFeatureNumbers[m] == msMinRemovedFeatureNo:
                    msMinIndex = m
                    break

            bestScores[msMinIndex] = score
            removedFeatureNumbers[msMinIndex] = removedFeatureNo
            bestSubsets[msMinIndex] = subset

        elif score == min(bestScores): # ss -> Abbreviation for Same Score
            removedFeatureNo = featureNo - len(featureList)
            ssIndices = [k for k, x in enumerate(bestScores) if x == score]
            ssRemovedFeatureNo = [removedFeatureNumbers[k] for k in ssIndices]
            ssMinRemovedFeatureNo = min(ssRemovedFeatureNo)
            
            if removedFeatureNo > ssMinRemovedFeatureNo:
                ssMinIndex = None

                for k in ssIndices:
                    if removedFeatureNumbers[k] == ssMinRemovedFeatureNo:
                        ssMinIndex = k
                        break

                removedFeatureNumbers[ssMinIndex] = removedFeatureNo
                bestSubsets[ssMinIndex] = subset

    localBestResults = list(zip(bestScores, removedFeatureNumbers, bestSubsets))
    gatheredResults = comm.gather(localBestResults, root = MASTER)

    if rank == MASTER:
        bestResults = []
        testAccuracyList = []
        featureNames = [] # A list to store names of the features included for each subset
        xColumns = list(x.columns) # Names of features

        for result in gatheredResults:
            bestResults += result
            
        bestResults.sort(reverse = True, key = operator.itemgetter(0,1))
        bestResults = bestResults[:topScoreNo]
        
        validationScores, removed, subsets = zip(*bestResults)
        
        for subset in subsets:
            featureList = []
            for j in range(featureNo):
                if subset[j] == '1':
                    featureList.append(j)
            
            mapping = map(xColumns.__getitem__, featureList) # Returns a mapping of the accessed indices
            featureNames.append(list(mapping))

            estimator.fit(x_train.iloc[:, list(featureList)], y_train)
            testAccuracy = estimator.score(x_test.iloc[:, list(featureList)], y_test)
            testAccuracyList.append(testAccuracy)
            
        bestResults = list(zip(testAccuracyList, validationScores, removed, subsets, featureNames))
        bestResults.sort(reverse = True, key = operator.itemgetter(0,2))
        accuracyList, cvScoreList, removedList, subsetList, featureNameList = zip(*bestResults)
        
    elapsedTime = MPI.Wtime() - startTime
    gatheredTimes = comm.gather(elapsedTime, root = MASTER)

    if rank == MASTER:
        with open(scoreResultFile, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['testAccuracy', 'cvScore', 'featureCount', 'subset', 'featureNames'])
            
            for i in range(topScoreNo):
                report = [accuracyList[i], cvScoreList[i], (featureNo - removedList[i]), subsetList[i], ('-'.join(featureNameList[i]))]
                writer.writerow(report)
                
        with open(timeResultFile, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['processNo', 'elapsedTime'])
            
            for i in range(size):
                report = [i, gatheredTimes[i]]
                writer.writerow(report)

def customSearch():
    pass

def estimatorFromStr(estimatorName): # Returns estimator object based on esimator name string parameter
    if estimatorName == 'gnb':
        return GaussianNB()
    elif estimatorName == 'bnb':
        return BernoulliNB()
    elif estimatorName == 'knnMinkowski':
        return KNeighborsClassifier(n_neighbors=5, metric='minkowski')
    elif estimatorName == 'knnEuclidean':
        return KNeighborsClassifier(n_neighbors=5, metric='euclidean')
    elif estimatorName == 'svcRbf':
        return SVC(kernel = 'rbf', gamma='scale')
    elif estimatorName == 'svcPoly':
        return SVC(kernel = 'poly', gamma='scale')
    elif estimatorName == 'logReg':
        return LogisticRegression(solver='liblinear', multi_class='auto')
    elif estimatorName == 'dtEntropy':
        return DecisionTreeClassifier(criterion='entropy', random_state = 1)
    elif estimatorName == 'dtGini':
        return DecisionTreeClassifier(criterion='gini', random_state = 1)
    elif estimatorName == 'rfEntropy':
        return RandomForestClassifier(n_estimators=10, criterion='entropy', random_state=1)
    elif estimatorName == 'rfGini':
        return RandomForestClassifier(n_estimators=10, criterion='gini', random_state=1)

if __name__ == '__main__':
    if len(sys.argv) == 10:
        try:
            datasetFileName = sys.argv[1]
            estimatorName = sys.argv[2]
            testSize = float(sys.argv[3])
            randomState = int(sys.argv[4])
            cv = int(sys.argv[5])
            topScoreNo = int(sys.argv[6])
            shuffle = bool(int(sys.argv[7]))
            timeResultFile = sys.argv[8]
            scoreResultFile = sys.argv[9]

            dataExtension = os.path.splitext(datasetFileName)[1]

            if dataExtension == '.csv':
                data = pd.read_csv(datasetFileName)            
            elif dataExtension == '.arff':
                with open(datasetFileName) as df:
                    data = a2p.load(df)
            elif dataExtension == '.xlsx':
                data = pd.read_excel(datasetFileName, engine='openpyxl')
            else:
                raise Exception('Invalid file extension!')

            estimator = estimatorFromStr(estimatorName)

            bruteForce(data=data, estimator=estimator, testSize=testSize, randomState=randomState, cv=cv, topScoreNo=topScoreNo, shuffle=shuffle, timeResultFile=timeResultFile, scoreResultFile=scoreResultFile)

        except Exception as e:
            print(e)
    
    else:
        print("Number of arguments is invalid!")