__author__ = 'sulantha'
import pandas as pd

class SurfStatsLinearModel:

    pvals = None
    tvals = None
    betas = None
    r_sqs = []

    def __init__(self, lmoObjectsList):
        self.__setPvals__(lmoObjectsList)
        self.__setTvals__(lmoObjectsList)
        self.__setBetas__(lmoObjectsList)
        self.__setRsqrs__(lmoObjectsList)

    def __setPvals__(self, lmoObjectsList):
        count = 0
        for lmo in lmoObjectsList:
            if self.pvals is None:
                self.pvals = pd.DataFrame(columns=[var for var in lmo.pvalues.index.values])
            self.pvals.loc[count] = lmo.pvalues.values.tolist()
            count += 1

    def __setTvals__(self, lmoObjectsList):
        count = 0
        for lmo in lmoObjectsList:
            if self.tvals is None:
                self.tvals = pd.DataFrame(columns=[var for var in lmo.tvalues.index.values])
            self.tvals.loc[count] = lmo.tvalues.values.tolist()
            count += 1

    def __setBetas__(self, lmoObjectsList):
        count = 0
        for lmo in lmoObjectsList:
            if self.params is None:
                self.params = pd.DataFrame(columns=[var for var in lmo.params.index.values])
            self.params.loc[count] = lmo.params.values.tolist()
            count += 1

    def __setRsqrs__(self, lmoObjectsList):
        for lmo in lmoObjectsList:
            self.r_sqs.append(lmo.rsquared)


    def print_stats(self):
        print(self.pvals.head(10))
        print(self.tvals.head(10))

