__author__ = 'sulantha'

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import pandas as pd
import statsmodels.formula.api as smf
import time
from SurfStatsLinearModel import SurfStatsLinearModel


multiValueRange = 40962


def readMultiValuedVars(fileList):
    return [open(f, 'r').readlines() for f in fileList]

def runLM(formulaString, dataTable, index):
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

t0 = time.time()
functionData = []

for i in range(multiValueRange):
    forTable = mainTable
    for k in multiValueVars:
        newVarColumn = [multiVarDict[k][0][x][i] for x in range(len(multiVarDict[k][0]))]
        forTable.loc[:, k] = [float(value.strip()) for value in newVarColumn]
    functionData.append([formulaString, forTable, i])

with ProcessPoolExecutor() as executor:
    executor.map(runLM, functionData)
    #pool.apply_async(runLM(formulaString, forTable, i))
    #est = smf.ols(formula=formulaString, data=forTable).fit()
    #lmoObjs[i] = est
t1 = time.time()
print('Time : {0}'.format(t1-t0))
sf = SurfStatsLinearModel(lmoObjs)
sf.print_stats()