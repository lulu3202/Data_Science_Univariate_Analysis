import pandas as pd
import numpy as np

class UniVariate():
    
    def QuanQual(dataset):
        Quan = []
        Qual = []
        for ColumnName in dataset.columns:
            print(ColumnName)
            if dataset[ColumnName].dtypes == "O":
                Qual.append(ColumnName)
            else:
                Quan.append(ColumnName)
        return Quan, Qual
    
    def UniVariate(dataset, Quan):
        descriptive = pd.DataFrame(
            index=["Mean", "Median", "Mode", "Q1:25%", "Q2:50%", "Q3:75%", "Q4:99%", "Q5:100%",
                   "IQR", "1.5Rule", "Lesser", "Greater", "Min", "Max", "Skewness", "Kurtosis",
                   "Variance", "Standard_Deviation"],
            columns=Quan)
        for ColumnName in Quan:
            descriptive[ColumnName]["Mean"]=dataset[ColumnName].mean()
            descriptive[ColumnName]["Median"]=dataset[ColumnName].median()
            descriptive[ColumnName]["Mode"]=dataset[ColumnName].mode()[0]
            descriptive[ColumnName]["Q1:25%"]=dataset.describe()[ColumnName]["25%"]
            descriptive[ColumnName]["Q2:50%"]=dataset.describe()[ColumnName]["50%"]
            descriptive[ColumnName]["Q3:75%"]=dataset.describe()[ColumnName]["75%"]
            descriptive[ColumnName]["Q4:99%"]=np.percentile(dataset[ColumnName],99)
            descriptive[ColumnName]["Q5:100%"]=dataset.describe()[ColumnName]["max"]
            descriptive[ColumnName]["IQR"]= descriptive[ColumnName]["Q3:75%"]-descriptive[ColumnName]["Q1:25%"]
            descriptive[ColumnName]["1.5Rule"]=1.5*descriptive[ColumnName]["IQR"]
            descriptive[ColumnName]["Lesser"]=descriptive[ColumnName]["Q1:25%"]-descriptive[ColumnName]["1.5Rule"]
            descriptive[ColumnName]["Greater"]=descriptive[ColumnName]["Q3:75%"]+descriptive[ColumnName]["1.5Rule"]
            descriptive[ColumnName]["Min"]=dataset[ColumnName].min()
            descriptive[ColumnName]["Max"]=dataset[ColumnName].max()
            descriptive[ColumnName]["Skewness"]=dataset[ColumnName].skew()
            descriptive[ColumnName]["Kurtosis"]=dataset[ColumnName].kurtosis()
            descriptive[ColumnName]["Variance"]=dataset[ColumnName].var()
            descriptive[ColumnName]["Standard_Deviation"]=dataset[ColumnName].std()
        return descriptive

    def FindingOutlier(Quan, descriptive):
        Lesser = []
        Greater = []
        for ColumnName in Quan:
            if descriptive[ColumnName]["Min"] < descriptive[ColumnName]["Lesser"]:
                Lesser.append(ColumnName)
            if descriptive[ColumnName]["Max"] > descriptive[ColumnName]["Greater"]:
                Greater.append(ColumnName)
        return Lesser, Greater
    
    def Handle_outliers(dataset, descriptive, Quan, Lesser, Greater):
        #Lesser, Greater = Finding_outliers(descriptive, Quan)
        for ColumnName in Lesser:
            dataset.loc[dataset[ColumnName] < descriptive[ColumnName]["Lesser"], ColumnName] = descriptive[ColumnName]["Lesser"]
        for ColumnName in Greater:
            dataset.loc[dataset[ColumnName] > descriptive[ColumnName]["Greater"], ColumnName] = descriptive[ColumnName]["Greater"]
        return dataset

    def FreqTable(ColumnName, dataset):
        FreqTable = pd.DataFrame(columns=["Unique_Values", "Frequency", "Relative_Frequency", "Cummulative_Frequency or cumsum"])
        FreqTable["Unique_Values"] = dataset[ColumnName].value_counts().index
        FreqTable["Frequency"] = dataset[ColumnName].value_counts().values
        total_count = len(dataset[ColumnName])
        FreqTable["Relative_Frequency"] = FreqTable["Frequency"] / total_count
        FreqTable["Cummulative_Frequency or cumsum"] = FreqTable["Relative_Frequency"].cumsum()
        return FreqTable