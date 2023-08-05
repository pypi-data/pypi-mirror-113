import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import pylab
import warnings
from termcolor import colored
warnings.filterwarnings("ignore")


def sturges(x):
    """
    Sturges method

    _____Parameters_____

    -x: feature

    _______Return_______

    -int: Best number of bins for the feature
    """
    import numpy as np
    N=len(x)
    sturges=int(np.ceil(1+np.log2(N)))
    return sturges

def missing_data(df, table=True, percentage=False, count=False, size=(10,6)):
    """
    Show missing values of the dataframe

    _____Parameters_____

    -df: dataframe

    -table: Bool
        If True, returns a dataframe. Default=True

    -percentage: Bool
        If True, show a graph of the missing values
        per feature with percentages. Default=False

    -count: Bool
        If True, show a graph of the missing values
        per feature with count. Default=False
    
    -size: Tuple. Optional
        Default=(10,6)

    _______Return_______

    Dataframe and graphs
    """
    
    total=df.isna().sum().sort_values(ascending=False)
    percent=df.isna().mean().sort_values(ascending=False)*100
    final=pd.concat([total, percent], axis=1, keys=['Total','Percent'])
    
    if(percentage):
        plt.figure(figsize=size)
        fig=final.Percent.plot.bar()
        plt.title("Missing Data Percentage",fontsize=20)
        plt.ylabel("Percentage",fontsize=15)
        plt.xlabel("Columns",fontsize=15)
        fig.axhline(y=5, color='red')
        plt.xticks(fontsize=14)
    
    
    
    if(count):
        plt.figure(figsize=size)
        fig=final.Total.plot.bar()
        plt.title("Total Missing Data",fontsize=20)
        plt.ylabel("Missing Data",fontsize=15)
        plt.xlabel("Columns",fontsize=15)
        plt.xticks(fontsize=14)
        
    if(table==True):
        return final


def value_counts(column, table=True, percentage=False, count=False, size=(10,6)):
    """
    Value counts for categorical features

    _____Parameters_____

    -column: feature

    -table: Bool
        If True, returns a dataframe. Default=True

    -percentage: Bool
        If True, show a graph of the missing values
        per feature with percentages. Default=False

    -count: Bool
        If True, show a graph of the missing values
        per feature with count. Default=False
    
    -size: Tuple. Optional
        Default=(10,6)

    _______Return_______

    Dataframe and graphs
    """
    
    total=column.value_counts()
    percent=column.value_counts()/len(column)*100
    final=pd.concat([total, percent], axis=1, keys=['Total','Percent'])
    
    if(percentage):
        plt.figure(figsize=size)
        fig=final.Percent.plot.bar()
        plt.title("Percentage of values",fontsize=20)
        plt.ylabel("Percentage",fontsize=15)
        fig.axhline(y=5, color='red')
        plt.xticks(fontsize=14)
    
    
    
    if(count):
        plt.figure(figsize=size)
        fig=final.Total.plot.bar()
        plt.title("Value count",fontsize=20)
        plt.ylabel("Count",fontsize=15)
        plt.xticks(fontsize=14)
        
    if(table==True):
        return final


def outliers(df, variable, method='IQR', limits=True, table=False):
    """
    Shows the outliers of a numerical feature

    _____Parameters_____

    -df: dataframe

    -variable: feature

    -method: String
        IQR, IQR3, std
    
    -limits: Bool
        If True, returns the limits of the IQR or IQR3
        Default=True

    -table: Bool
        If True, returns a dataframe. Default=False

    _______Return_______

    Dataframe
    """
    if(method=='std'):
        upper_boundary = df[variable].mean() + 3 * df[variable].std()
        lower_boundary = df[variable].mean() - 3 * df[variable].std()
        if(limits):
            print("MIN: {}\nMAX: {}".format(lower_boundary,upper_boundary))
        if(table):
            outliers=df.loc[(df[variable]<lower_boundary)|(df[variable]>upper_boundary),]
            return outliers
    
    if(method=='IQR'):
        IQR = df[variable].quantile(0.75) - df[variable].quantile(0.25)
        lower_boundary = df[variable].quantile(0.25) - (IQR * 1.5)
        upper_boundary = df[variable].quantile(0.75) + (IQR * 1.5)
        if(limits):
            print("MIN: {}\nMAX: {}".format(lower_boundary,upper_boundary))
        if(table):
            outliers=df.loc[(df[variable]<lower_boundary)|(df[variable]>upper_boundary),]
            return outliers
    
    if(method=='IQR3'):
        IQR = df[variable].quantile(0.75) - df[variable].quantile(0.25)
        lower_boundary = df[variable].quantile(0.25) - (IQR * 3)
        upper_boundary = df[variable].quantile(0.75) + (IQR * 3)
        if(limits):
            print("MIN: {}\nMAX: {}".format(lower_boundary,upper_boundary))
        if(table):
            outliers=df.loc[(df[variable]<lower_boundary)|(df[variable]>upper_boundary),]
            return outliers
    

def distribution_diag(df, variable, size=(20,5)):
    """
    Displays three graphs to allow understand 
    the feature

    _____Parameters_____

    -df: dataframe

    -variable: feature
    
    -size: Tuple. Optional
        Default=(20,5)

    _______Return_______

    graphs
    """
    plt.figure(figsize=size)

    plt.subplot(1, 3, 1)
    sns.distplot(df[variable], bins=sturges(df[variable]))
    mean=df[variable].mean()
    median=df[variable].median()
    plt.axvline(mean, color='r', linestyle='dashed',alpha=0.4)
    plt.axvline(median, color='k', linestyle='dashed',alpha=0.4)
    plt.title('Histogram')

    plt.subplot(1, 3, 2)
    stats.probplot(df[variable], dist="norm", plot=plt)
    plt.ylabel('{} quantiles'.format(variable))
    plt.title('Probability Plot')

    plt.subplot(1, 3, 3)
    sns.boxplot(y=df[variable])
    plt.title('Boxplot')

    plt.show


def correlation(df,variable):
    """
    Display the correlation of the feature with
    the other features of the dataframe

    _____Parameters_____

    -df: dataframe

    -variable: feature

    _______Return_______

    Dataframe
    """
    corr=df.corr()
    x=corr[[variable]].sort_values(by=variable,ascending=False)\
    .style.background_gradient()
    return x


def corr_plot(x):
    """
    Display a graph of correlation of all features

    _____Parameters_____

    -x: dataframe

    _______Return_______

    graph
    """
    corr=x.corr()
    mask = np.triu(np.ones_like(corr, dtype=np.bool))
    f, ax = plt.subplots(figsize=(12,6))
    cmap = sns.color_palette("PRGn",10)
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1,vmin=-1, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5},annot=True)
    plt.show()

def project_checklist():
    print('Frame the problem')
    print('\t-Define the objective')
    print('\t-Supervised/Unsupervised, online/offline')
    print('\t-Measure of the performance')
    print('\t-Minimum performance needed to reach the objective')
    print('\t-Assumptions\n')
    print('Get the data')
    print('\t-Document where is the data')
    print('\t-Check how much space it takes')
    print('\t-Check legal obligations and get authorization')
    print('\t-Create a workspace')
    print('\t-Convert the data to a good format')
    print('\t-Delete or protect sensitive information')
    print('\t-Check the type of data')
    print('\t-Put a test set aside\n')
    print('Explore the data')
    print('\t-Create a copy of the data for exploration')
    print('\t-Study each attribute')
    print('\t-Identify the target attribute if supervised learning')
    print('\t-Visualize the data')
    print('\t-Study the correlations')
    print('\t-Identify the transformations you need')
    print('\t-Document what you have learned')
    print('\nPrepare the data')
    print('\t-Work on copies of the data')
    print('\t-Write functions for all transformations')
    print('\t-Data cleaning (outliers and missing values)')
    print('\t-Feature selection (Drop attributes with no useful information)')
    print('\t-Feature engineering (Discretize, Decompose, etc)')
    print('\t-Feature scaling (standardize, normalize)')
    print('\nShortlist promising models')
    print('\t-Automate this steps as much as posible')
    print('\t-Train many quick-and-dirty models using standar parameters')
    print('\t-Measure and compare the performance with N-fold CV and compute the mean and sd of the performances')
    print('\t-Analyze the most significant variables for each algorithm')
    print('\t-Analyze the type of errors the models make')
    print('\t-Shortlist the top promising models')
    print('\nFine-Tune the system')
    print('\t-Fine-Tune hyperparameters using CV')
    print('\t-Random Search > Grid Search unless very few hyperparameters to explore')
    print('\t-If training is very long, use Bayesian optimization approach')
    print('\t-Use ensemble methods for better performance')
    print('\t-Measure model performance on the test set to get the generalization error')
    print('\nPresent your solution')
    print('\t-Document what you have done')
    print('\t-Create a nice presentation')
    print('\t-Explain why the solution archieves the objective')
    print('\t-Present interesting points and key findings')
    print('Launch')
    print('\t-Get the solution ready to production')
    print('\t-Write monitoring code and trigger alerts')


def feature_analysis(df,feature,test=None,target=None):
    """
    Feature summary

    _____Parameters_____

    -df: dataframe

    -feature: feature
    
    -test: dataframe. Optional

    -target: feature. Optional

    _______Return_______

    summary
    """
    numdata = ['int64','float64']
    #NUMERICA
    if(df[feature].dtype in numdata):
        print(f"The feature {feature} is NUMERIC\n")
        
        if(df[feature].isna().sum()==0):
            print(colored(f'-Missing values in training set: {df[feature].isna().sum()}','green'))
        if(df[feature].isna().sum()!=0):
            print(colored(f'-Missing values in training set: {df[feature].isna().sum()}','red'))
        if (test is not None):
            if(feature!=target):
                if(test[feature].isna().sum()==0):
                    print(colored(f'-Missing values in test set    : {test[feature].isna().sum()}','green'))
                if(test[feature].isna().sum()!=0):
                    print(colored(f'-Missing values in test set    : {test[feature].isna().sum()}','red'))
        
        if(outliers(df,feature,limits=False,table=True,method='IQR').shape[0]==0):
            print(colored(f"-Outliers 1.5*IQR: {outliers(df,feature,limits=False,table=True,method='IQR').shape[0]}",'green'))
        if(outliers(df,feature,limits=False,table=True,method='IQR').shape[0]!=0):
            print(colored(f"-Outliers 1.5*IQR: {outliers(df,feature,limits=False,table=True,method='IQR').shape[0]}",'yellow'))
        if(outliers(df,feature,limits=False,table=True,method='IQR3').shape[0]==0):
            print(colored(f"-Outliers   3*IQR: {outliers(df,feature,limits=False,table=True,method='IQR3').shape[0]}",'green'))
        if(outliers(df,feature,limits=False,table=True,method='IQR3').shape[0]!=0):
            print(colored(f"-Outliers   3*IQR: {outliers(df,feature,limits=False,table=True,method='IQR3').shape[0]}",'red'))
        
        distribution_diag(df,feature)
        plt.show()
    
    #CATEGORICA
    if(df[feature].dtype not in numdata):
        print(f"The feature {feature} is CATEGORICAL\n")
        
        if(len(df[feature].unique())<=20):
            print(colored(f'-Cardinality: {len(df[feature].unique())}','green'))
        if(len(df[feature].unique())>20):
            print(colored(f'-Cardinality: {len(df[feature].unique())}','red'))
        
        if(df[feature].isna().sum()==0):
            print(colored(f'-Missing values in training set: {df[feature].isna().sum()}','green'))
        if(df[feature].isna().sum()!=0):
            print(colored(f'-Missing values in training set: {df[feature].isna().sum()}','red'))
        if (test is not None):
            if(feature!=target):
                if(test[feature].isna().sum()==0):
                    print(colored(f'-Missing values in test set    : {test[feature].isna().sum()}','green'))
                if(test[feature].isna().sum()!=0):
                    print(colored(f'-Missing values in test set    : {test[feature].isna().sum()}','red'))
        
        if(len(df[feature].unique())<=20):
            value_counts(df[feature],percentage=True)
            plt.show()
        if(len(df[feature].unique())>20):
            print(colored('-THE CARDINALITY IS TOO BIG','red'))


def dataset_analysis(df,target,test=None):
    """
    dataframe summary

    _____Parameters_____

    -df: dataframe

    -target: feature
    
    -test: dataframe. Optional

    _______Return_______

    summary
    """
    columnas =  df.columns.to_list()
    numdata = ['int64','float64']
    print('  ')
    if(df.duplicated().sum()==0):
        print(colored(f'Duplicated rows: {df.duplicated().sum()}','green'))
    if(df.duplicated().sum()!=0):
        print(colored(f'Duplicated rows: {df.duplicated().sum()}','red'))
    print()
    corr_plot(df)
    plt.show()
    
    
    for i,x in enumerate(columnas):
        print("_"*150)
        print('\n')
        print(colored(f"{x.upper().center(140,' ')}",'cyan'))
        print(f"\nFeature number {i}:\t{x}\n")
        
        feature_analysis(df,x,test,target)