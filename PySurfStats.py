__author__ = 'sulantha'

import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from concurrent.futures import ThreadPoolExecutor

from SurfStatsLinearModel import SurfStatsLinearModel

multiValueRange = 40962
executor = ThreadPoolExecutor(max_workers=10)

def readMultiValuedVars(fileList):
    return [open(f, 'r').readlines() for f in fileList]

def runLM(formulaString, dataTable, index):
    print('Running : {0}'.format(index))
    global lmoObjs
    lmoObjs[index] = smf.ols(formula=formulaString, data=dataTable).fit()

fullTable = pd.read_csv('TestData/testDataGlim.csv')

queryString = 'diagnosis == \'CN\' '
columnList = ['ID', 'diagnosis']
mainTable = fullTable.query(queryString)


formulaString = 'Av45_bl_left_diffBlur ~ Av45_bl_right_diffBlur+Age_bl'

multiValueVars = ['Av45_bl_left_diffBlur', 'Av45_bl_right_diffBlur']
multiVarDict = {var: [readMultiValuedVars(mainTable[var])] for var in multiValueVars}

lmoObjs = [0]*multiValueRange

for i in range(multiValueRange):
    forTable = mainTable
    for k in multiValueVars:
        newVarColumn = [multiVarDict[k][0][x][i] for x in range(len(multiVarDict[k][0]))]
        forTable.loc[:, k] = [float(value.strip()) for value in newVarColumn]
    executor.submit(runLM(formulaString, forTable, i))
    #est = smf.ols(formula=formulaString, data=forTable).fit()
    #lmoObjs[i] = est


sf = SurfStatsLinearModel(lmoObjs)