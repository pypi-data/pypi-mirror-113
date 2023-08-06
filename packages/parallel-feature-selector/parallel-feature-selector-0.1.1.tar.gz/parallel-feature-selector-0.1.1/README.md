# Parallel Feature Selector
A feature selection module that works in parallel among the processors

## Installation

```
pip install parallel-feature-selector
```

Dependencies:
- pandas
- scikit-learn
- mpi4py
- arff2pandas
- openpyxl

MPI needs to be installed on the computer.
For Windows:
- Install both Microsoft MPI v10.0 and Microsoft MPI SDK
- Set up environment variables
-- C:\Program Files (x86)\Microsoft SDKs\MPI
-- C:\Program Files\Microsoft MPI\Bin
- Install mpi4py with "conda install -c intel mpi4py" in Anaconda Prompt

## Usage (Module)

Example Code:
```
import parallel_feature_selector as pfs
pfs.bruteForce(data, estimator, 0.2, 42, 10, 10, True, 'outputTimeAnalysis.csv', 'outputSubsetAnalysis.csv')
```

Function Parameters and Default Arguments:
```
def bruteForce(data, estimator, testSize=0.2, randomState=42, cv=5, topScoreNo=5, shuffle=True, timeResultFile='outputTimeAnalysis.csv', scoreResultFile='outputSubsetAnalysis.csv')
```

| Parameter | Description |
| ------ | ------ |
| data | pandas.DataFrame with column names and numerical values |
| esimator | scikit-learn esimator object |
| testSize | float, test size between 0 and 1 for train_test_split (Default = 0.2) |
| randomState | int or None, random state for train_test_split (Default = 42) |
| cv | int, fold number for cross-validation (Default = 5) |
| topScoreNo | int, specifies how many best-scoring subsets to print (Default = 5) |
| shuffle | bool, used to shuffle the data set before splitting (Default = True) |
| timeResultFile | Output file path for elapsed time results in csv format (Default = 'outputTimeAnalysis.csv') |
| scoreResultFile | Output file path for score and subset results in csv format (Default = 'outputSubsetAnalysis.csv') | 

# Usage (Script)

You can also run the code in terminal with the following arguments:
```
mpiexec -n [PROCESS_NO] python parallel_feature_selector.py [DATA_SET_PATH] [ESTIMATOR_NAME] [TEST_SIZE] [RANDOM_STATE] [CROSS_VALIDATION] [TOP_SCORE_NO] [SHUFFLE] [TIME_RESULT_PATH] [SCORE_RESULT_PATH]
```

- [RANDOM_STATE] must be given as integer ('None' can be given in module function)
- [SHUFFLE] must be given as integer, 1 for 'True' and 0 for 'False' ('True' or 'False' in module function)

Example:
```
mpiexec -n 4 python parallel_feature_selector.py C:\Users\BILGISAYAR\Desktop\AcademicPerformance.csv gnb 0.2 1 10 10 1 outputTimeAnalysis.csv outputSubsetAnalysis.csv
```

When running the script in terminal:
- .csv .xlsx .arff files can be used for input data set
- Available estimator arguments: gnb, bnb, knnMinkowski, knnEuclidean, svcRbf, svcPoly, logReg, dtEntropy, dtGini, rfEntropy, rfGini

| Terminal Argument | Scikit-Learn Estimator |
| ------ | ------ |
| gnb | GaussianNB() | 
| bnb | BernoulliNB() |
| knnMinkowski | KNeighborsClassifier(n_neighbors=5, metric='minkowski') |
| knnEuclidean | KNeighborsClassifier(n_neighbors=5, metric='euclidean') |
| svcRbf | SVC(kernel = 'rbf', gamma='scale') |
| svcPoly | SVC(kernel = 'poly', gamma='scale') |
| logReg | LogisticRegression(solver='liblinear', multi_class='auto') |
| dtEntropy | DecisionTreeClassifier(criterion='entropy', random_state = 1) |
| dtGini | DecisionTreeClassifier(criterion='gini', random_state = 1) |
| rfEntropy | RandomForestClassifier(n_estimators=10, criterion='entropy', random_state=1) |
| rfGini | RandomForestClassifier(n_estimators=10, criterion='gini', random_state=1) |
