# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 12:49:56 2020

@author: Jiyuan Zhang
"""
# %% Load Files 
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


Demographic=pd.read_csv('Demographic_201801_201910.csv')
Orders=pd.read_csv('Orders_201801_201910.csv')
Product=pd.read_csv('Product_201801_201910.csv')
Usage=pd.read_csv('Usage_201801_201910.csv')


Demographic1=Demographic.copy()
Orders1=Orders.copy()
Product1=Product.copy()
Usage1=Usage.copy()


# %% Export original files to CSV 
#Demographic1.head(5000).to_csv('sample1_head_5000_of_demographic1.csv',index=False)
#Demographic1.tail(5000).to_csv('sample1_tail_5000_of_demographic1.csv',index=False)
#Orders1.head(5000).to_csv('sample1_head_5000_of_Orders1.csv',index=False)
#Orders1.tail(5000).to_csv('sample1_tail_5000_of_Orders1.csv',index=False)
#Product1.head(5000).to_csv('sample1_head_5000_of_Product1.csv',index=False)
#Product1.tail(5000).to_csv('sample1_tail_5000_of_Product1.csv',index=False)
#Usage1.head(5000).to_csv('sample1_head_5000_of_Usage1.csv',index=False)
#Usage1.tail(5000).to_csv('sample1_tail_5000_of_Usage1.csv',index=False)



# %% Explore all tables
Orders1['MonthKey'].max() 
#20191001
Orders1['MonthKey'].min()
#20180101

Product1['MonthKey'].max() 
#20191001
Product1['MonthKey'].min() 
#20180101
Usage1['MonthKey'].max() 
#20191001
Usage1['MonthKey'].min() 
#20180101

Demographic1['CustomerNodeId'].value_counts()  #808640
Orders1['CustomerNodeId'].value_counts()       #808640
Product1['CustomerNodeId'].value_counts()      #808640
Usage1['CustomerNodeId'].value_counts()        #808640

Demographic1['CustomerNodeId'].isin(Orders1['CustomerNodeId']).value_counts() #True
Orders1['CustomerNodeId'].isin(Demographic1['CustomerNodeId']).value_counts() #True

### All files have same CustomerNodeId


A=Orders1[['CustomerNodeId','MonthKey']].groupby('CustomerNodeId').count().reset_index()
B=Product1[['CustomerNodeId','MonthKey']].groupby('CustomerNodeId').count().reset_index()
C=Usage1[['CustomerNodeId','MonthKey']].groupby('CustomerNodeId').count().reset_index()

(A==B)['MonthKey'].value_counts()
(A==C)['MonthKey'].value_counts()
(C==B)['MonthKey'].value_counts()

###Except the Demographic, others MonthKey are match, demographic does no have MonthKey

### CustomerNodeId and it's lenght of the history
Customer_history_length=Orders1[['CustomerNodeId','MonthKey']].groupby('CustomerNodeId').count().reset_index()
#        CustomerNodeId  MonthKey
#0              1040415        22
#1              1040416        22
#2              1040417        22
#3              1040418        22
#4              1040422        22
#               ...       ...
#808635         3830761         1
#808636         3830791         1
#808637         3830829         1
#808638         3830851         1
#808639         3830895         1


### The 7530 customers only have 1 month history record
Product1[['CustomerNodeId','MonthKey']].groupby('CustomerNodeId').count().reset_index()['MonthKey'].value_counts().sort_index()
#1       7530
#2       9601
#3      12337
#4      11460
#5       9950
#6       9785
#7       8829                          Those number has total of 808640
#8       9631
#9       9178
#10     10029
#11      8743
#12      9982
#13      9872
#14      9755
#15     13208
#16    112951
#17      9064
#18      8079
#19      6958
#20      8070
#21      7477
#22    506151


# %% Subset Files 

### customers_with_22_month_history
customers_with_22_month_history=Customer_history_length[Customer_history_length['MonthKey']==22][['CustomerNodeId']]
customers_with_22_month_history.to_csv('customers_with_22_month_history.csv',index=False)
#506151 rows
customers_without_22_month_history=Customer_history_length[Customer_history_length['MonthKey']<22][['CustomerNodeId']]
customers_without_22_month_history.to_csv('customers_without_22_month_history.csv',index=False)
#302489 rows

#
#
#Demographic2=pd.merge(customers_with_22_month_history, Demographic1,how='inner',left_on='CustomerNodeId',right_on='CustomerNodeId')
#len(Demographic2['CustomerNodeId'].unique())
#Demographic2.to_csv('Demographic2.csv',index=False)
#
#Orders2=pd.merge(customers_with_22_month_history, Orders1,how='inner',left_on='CustomerNodeId',right_on='CustomerNodeId')
#len(Orders2['CustomerNodeId'].unique())
#Orders2.to_csv('Orders2.csv',index=False)


#
#Product2=pd.merge(customers_with_22_month_history, Product1,how='inner',left_on='CustomerNodeId',right_on='CustomerNodeId')
#len(Product2['CustomerNodeId'].unique())
#Product2.to_csv('Product2.csv',index=False)
#
#Usage2=pd.merge(customers_with_22_month_history, Usage1,how='inner',left_on='CustomerNodeId',right_on='CustomerNodeId')
#len(Usage2['CustomerNodeId'].unique())
#Usage2.to_csv('Usage2.csv',index=False)


### Read file that contain customers record having 22 months

506151/808640*100
### 62.59
### Read 62.59 percents of total file
Demographic2=pd.read_csv('Demographic2.csv')
Orders2=pd.read_csv('Orders2.csv')
Product2=pd.read_csv('Product2.csv')
Usage2=pd.read_csv('Usage2.csv')




## to get the excel file that has each customer's overaltenure of customer who churned
jjjj=Demographic2[['CustomerNodeId','OverallTenure']][Demographic2['CustomerNodeId'].isin(customer_churn_at_packge['CustomerNodeId'])]
jjjj=jjjj.groupby('CustomerNodeId').apply(lambda x: np.max(x))

jjjj.to_csv('CustomerOverallTenure.csv',index=False)

# %% Product 1


### Product1 column names
list(Product1.columns)
#['CustomerNodeId',
# 'MonthKey',
# 'HasHsd',
# 'HasVideo',
# 'HasPhone',
# 'PackageCount',
# 'PackageName',
# 'PackageTotalCost',
# 'OnPromotion',
# 'PromotionLengthInMonths',
# 'PromotionLengthInDays',
# 'PromotionDaysRemaining',
# 'TopLevelOfferCount',
# 'ProductOfferCount',
# 'CurrentMRC',
# 'HasNonStandardRate']

### PackageName
Product1['PackageName'].value_counts()
#I       8256862
#IV      2480346
#none    2299013
#VIP     1150508
#IP       622545
#V         75581
#VP        16441
#P         10140

###Customer_package_length
Product1_Customer_package_length=Product1[['CustomerNodeId','PackageName','MonthKey']].groupby(['CustomerNodeId','PackageName']).count().reset_index()
Product1_Customer_package_length.rename(columns={'MonthKey':'length'},inplace=True)
#      CustomerNodeId PackageName  length
#0          1040415          IP       1
#1          1040415           P      10
#2          1040415        none      11
#3          1040416           I       5
#4          1040416        none      17
#5          1040417           I      15
#6          1040417        none       7
#7          1040418           I      22
#8          1040422           I      22
#9          1040423           I      20
#10         1040423          IP       2
#11         1040429         VIP      22



#for i in Product1.columns:
#    print(i)
#    print(Product1[i].value_counts())
    
    
Product1[['CustomerNodeId','CurrentMRC']].groupby('CustomerNodeId').agg(np.nanmean).sort_values(by='CurrentMRC',ascending=False)

#CustomerNodeId  CurrentMRC   
#3588239         1815.063750
#3588946         1799.940000
### Those two customers have very high CurrentMRC #3588239 #3588946 


#Product1.loc[Product1['CustomerNodeId']==3588239]['MonthKey']
#Product1.loc[Product1['CustomerNodeId']==3588239]['CurrentMRC']
#Product1.loc[Product1['CustomerNodeId']==3588946]
#
#plt.bar(x=Product1.loc[Product1['CustomerNodeId']==3588239]['MonthKey'],height=Product1.loc[Product1['CustomerNodeId']==3588239]['CurrentMRC'],width=0.35)

Product1[['PackageName','MonthKey']].groupby('PackageName').count()



# %%  Demographic1

### Demographic1 column names
list(Demographic1.columns)
#['CustomerNodeId',
# 'FinancialSystemName',
# 'FranchiseTaxArea',
# 'OverallTenure',
# 'PreviousActiveDays',
# 'LifeTimeValue',
# 'CustomerStatus',
# 'SubscriberwiseScore',
# 'HasDepositAccount',
# 'LastDisconnectDate',
# 'LastInstallDate',
# 'OriginalInstallDate',
# 'ConneXionsClusterName',
# 'ConneXionsLifestageName',
# 'Dwelling',
# 'OperatingCenterNumber',
# 'ServiceCity',
# 'ServiceState',
# 'CustomerType',
# 'HsdServiceable',
# 'VideoServiceable',
# 'PhoneServiceable']

### States columns
Demographic1['ServiceState'].value_counts()   # 22 States
#ID    3864048
#MS    1985658
#TX    1958237
#AZ    1566130
#OK    1047807
#MO     679008
#IL     650686
#AL     445975
#NM     443950
#IN     428732
#IA     423771
#ND     333794
#NE     206546
#KS     193711
#LA     172339
#AR     160698
#WA     111307
#TN     100976
#MN      63430
#OR      43405
#SD      31227
#CA          1

### CustomerType
Demographic1['CustomerType'].value_counts()  # 3 types 
#Residential      14903552
#Business             7878
#Business Bulk           6



#Demographic1[['CustomerNodeId','FinancialSystemName','ServiceState']].groupby('CustomerNodeId').count().to_csv('How_many_row_of_each_customer.csv',index=False)


Total_unique_CustomerNodeId=list(Demographic1['CustomerNodeId'].unique())

First_50_of_CustomerNodeId=Total_unique_CustomerNodeId[0:404320].copy()
## can not in the name 
Second_50_of_CustomerNodeId=Total_unique_CustomerNodeId[404320:].copy()

## I seperate the entire demographic data into 2 parts 

Demographic1['CustomerNodeId'].isin(First_50_of_CustomerNodeId)

#First_50=Demographic1.loc[Demographic1['CustomerNodeId'].isin(First_50_of_CustomerNodeId)].copy()
#Second_50=Demographic1.loc[Demographic1['CustomerNodeId'].isin(Second_50_of_CustomerNodeId)].copy()
#First_50.to_csv('first50%Demograpgic.csv',index=False)
#Second_50.to_csv('Second50%Demograpgic.csv',index=False)
#
#
#
#
#

### CustomerStatus
Demographic1['CustomerStatus'].value_counts()
#Active                12669086
#Disconnect             2183955
#Pending Activation       58113
#Natural Disaster           282
Demographic1['CustomerStatus'].value_counts()/Demographic1.shape[0]
#Active                0.849622
#Disconnect            0.146462
#Pending Activation    0.003897
#Natural Disaster      0.000019
####above have a lot repeated values!!! remember so customer have more than one statues 

#Demographic1['CustomerStatus'].unique()
#for i in Demographic1['CustomerStatus'].unique():
#    print(i)
#    print(len(Demographic1['CustomerNodeId'][Demographic1['CustomerStatus']==i].unique())/len(Demographic1['CustomerNodeId'].unique()))

#Active
#808637/////0.9999962900672734
#Disconnect
#220162/////0.2722620696478037
#Pending Activation
#41254/////0.05101652156707558
#Natural Disaster
#44/////5.441234665611397e-05
### still!! there are repeated customerStatus, the percentage proved that 

Customers_different_status_count=Demographic1[['CustomerNodeId','CustomerStatus','FranchiseTaxArea']].groupby(['CustomerNodeId','CustomerStatus']).count().reset_index().rename(columns={'FranchiseTaxArea':'status_count'})
#         CustomerNodeId CustomerStatus  status_count
#0               1040415         Active            11
#1               1040415     Disconnect            11
#2               1040416         Active             5
#3               1040416     Disconnect            17
#4               1040417         Active            15


Customers_different_status_count['CustomerStatus'].value_counts()
#Active                808637
#Disconnect            220162
#Pending Activation     41254
#Natural Disaster          44

### get customers that have experienced Natural Diaster
Customer_experiences_Natural_Disaster=[Demographic1['CustomerNodeId'][Demographic1['CustomerStatus']=='Natural Disaster'].unique()]





Customers_status_count=Demographic1[['CustomerNodeId','CustomerStatus','FranchiseTaxArea']].groupby(['CustomerNodeId','CustomerStatus']).count().reset_index().groupby('CustomerNodeId').count().reset_index()
Customers_status_count.drop('FranchiseTaxArea',axis='columns',inplace=True)
Customers_status_count.rename(columns={'CustomerStatus':'Different_status_count'},inplace=True)
###show how many different Status of each customer
#          CustomerNodeId  Different_status_count
#0              1040415                       2
#1              1040416                       2
#2              1040417                       2
#3              1040418                       1
#4              1040422                       1  

len(Customers_status_count[Customers_status_count['Different_status_count']>=2])
#245982/808640=0.30     30% of customer who has 2 and more status has natural diaster

# %% Demographic 2

### Some customers have more one one state information 
number_of_unique_state=Demographic2[['CustomerNodeId','ServiceState']].groupby('CustomerNodeId').agg({'ServiceState':pd.Series.nunique})
number_of_unique_state=number_of_unique_state.reset_index()

number_of_unique_state.rename({'ServiceState':'count_of_ServiceState'},inplace=True)

number_of_unique_state.to_csv('number_of_unique_state.csv',index=False)
number_of_unique_state.shape    #(506151, 2)

pd.read_csv('number_of_unique_state.csv')

Demographic2['ServiceState'].value_counts()






len(number_of_unique_state[number_of_unique_state['ServiceState']>1])

number_of_unique_state['CustomerNodeId'][number_of_unique_state['ServiceState']>1].to_csv('customers_move_to_diff_state.csv',index=False)

#  1718  rows 




# %% Product 2
len(Product2['CustomerNodeId'].unique())
Product2['PackageName'].value_counts()
#I       6021357
#IV      1864513
#none    1715523
#VIP      920729
#IP       526450
#V         62901
#VP        14664
#P          9185
Demographic2['CustomerStatus'].value_counts()
#Active                9447820
#Disconnect            1668402
#Pending Activation      18824
#Natural Disaster          276





#Demographic2.loc[Demographic2['CustomerNodeId']==1040417]['CustomerStatus']


Product2_Customer_package_length=Product2[['CustomerNodeId','PackageName','MonthKey']].groupby(['CustomerNodeId','PackageName']).count().reset_index()
#        CustomerNodeId PackageName  MonthKey
#0              1040415          IP         1
#1              1040415           P        10
#2              1040415        none        11                  [719660 rows x 3 columns]
#3              1040416           I         5                  506151 different customers
#4              1040416        none        17
#               ...         ...       ...
#719655         3086805        none         1
#719656         3086806           I        17
#719657         3086806        none         5
#719658         3086807           I        21
#719659         3086807        none         1    


###Product2_number_of_different_packages_of_each_customer includes none 
Product2_number_of_different_packages_of_each_customer=Product2_Customer_package_length.groupby('CustomerNodeId').count().reset_index()
                                                        #506151 different customers
#        CustomerNodeId  PackageName  MonthKey
#0              1040415            3         3
#1              1040416            2         2
#2              1040417            2         2
#3              1040418            1         1
#4              1040422            1         1
#               ...          ...       ...
#506146         3086803            2         2
#506147         3086804            2         2
#506148         3086805            2         2
#506149         3086806            2         2
#506150         3086807            2         2



### Which means that not all customer who has 2 or more different packages has the none package.
D=Product2_Customer_package_length['CustomerNodeId'][Product2_Customer_package_length['PackageName']=='none'].unique()
len(D) #152724
E=Product2_number_of_different_packages_of_each_customer['CustomerNodeId'][Product2_number_of_different_packages_of_each_customer['PackageName']>=2].unique()
len(E) #195631
### 只是用来检测




### the fiist day of each package, 1040417 is special, has none first then I package   #506151 rows 
customers_churn_date_of_different_package=Product2.groupby(['CustomerNodeId','PackageName']).apply(lambda x:x['MonthKey'].min()).reset_index()
customers_churn_date_of_different_package.head(200)
len(customers_churn_date_of_different_package['CustomerNodeId'].unique())    #506151 customers
#        CustomerNodeId PackageName         0
#0              1040415          IP  20180101
#1              1040415           P  20180201
#2              1040415        none  20181201
#3              1040416           I  20180101         [719660 rows x 3 columns]
#4              1040416        none  20180601
#5              1040417           I  20180801
#6              1040417        none  20180101          #1040417 has the none first then has package
#7              1040418           I  20180101
#8               1040422           I  20180101
#9               1040423           I  20180301              ...         ...       ...
#719655         3086805        none  20180101
#719656         3086806           I  20180201
#719657         3086806        none  20180101
#719658         3086807           I  20180201
#719659         3086807        none  20180101

customers_churn_date_of_different_package.to_csv('customers_change_packages.csv',index=False)



### customers that has none in customers_churn_date_of_different_package,subset from previous table
customers_that_has_none_in_customers_churn_date_of_different_package=customers_churn_date_of_different_package[customers_churn_date_of_different_package['CustomerNodeId'].isin(customers_churn_date_of_different_package[customers_churn_date_of_different_package['PackageName']=='none']['CustomerNodeId'])]
# 321074 rows
len(customers_that_has_none_in_customers_churn_date_of_different_package['CustomerNodeId'].unique())  
# 152724 customers
customers_that_has_none_in_customers_churn_date_of_different_package.tail(20)

#        CustomerNodeId PackageName         0
#0              1040415          IP  20180101
#1              1040415           P  20180201
#2              1040415        none  20181201
#3              1040416           I  20180101
#4              1040416        none  20180601
#5              1040417           I  20180801
#6              1040417        none  20180101
#21             1040454          IP  20180101
#22             1040454        none  20181001
#34             1040471          IP  20180101
#35             1040471        none  20190101
#               ...         ...       ...
#719648         3086802           I  20180201
#719649         3086802        none  20180101
#719650         3086803           I  20180201
#719651         3086803        none  20180101
#719652         3086804           I  20180201
#719653         3086804        none  20180101
#719654         3086805           I  20180201
#719655         3086805        none  20180101
#719656         3086806           I  20180201
#719657         3086806        none  20180101
#719658         3086807           I  20180201
#719659         3086807        none  20180101






### customers churn date, assuming customer had packages first then churn, however 1040417 none first, then has package 
### give us the first none day of each customer who has none in product name 
customers_first_none_productname_date=Product2[Product2['PackageName']=='none'].groupby('CustomerNodeId').apply(lambda x:x['MonthKey'].min()).reset_index()
customers_first_none_productname_date.rename(columns={0:'MonthKey'},inplace=True)
customers_first_none_productname_date.head(20)
                                                       #152724 Rows 
#        CustomerNodeId  MonthKey
#0              1040415  20181201
#1              1040416  20180601
#2              1040417  20180101
#3              1040454  20181001
#4              1040471  20190101
#5              1040479  20180301
#6              1040481  20180901
#7              1040483  20181201
#8              1040486  20190701
#9              1040500  20190801
#10             1040522  20180301
#11             1040524  20190501
#12             1040525  20180901
#13             1040533  20180101
#14             1040552  20190701
#15             1040556  20190601
#16             1040557  20180901
#17             1040572  20181201
#18             1040573  20190901
#19             1040580  20190601
#               ...       ...
#152719         3086803  20180101
#152720         3086804  20180101
#152721         3086805  20180101
#152722         3086806  20180101
#152723         3086807  20180101




### customers that change from none active to active, the MonthKey is there first none date
# those whose monthkey is not 1/1, has some special patterns, such as avtive to non active to active 
# 这个的逻辑是，如果看下每个customer 的package里面，第一次用每个package的最大的日期是什么。如果这个最大日期就是这个customer 用none 的日期，那么这个customer肯定就是从non-active 变成 active                                                        
ooo=customers_that_has_none_in_customers_churn_date_of_different_package.groupby('CustomerNodeId').apply(lambda x: x[0].max()).reset_index()
customers_none_active_to_active=customers_first_none_productname_date[ooo[0]!=customers_first_none_productname_date['MonthKey']]
                                     #29897 rows 
#2              1040417  20180101        # the execonf column does not have any meaning 
#13             1040533  20180101
#27             1040624  20180101
#31             1040658  20180101
#32             1040668  20180501
#               ...       ...
#152719         3086803  20180101
#152720         3086804  20180101
#152721         3086805  20180101
#152722         3086806  20180101
#152723         3086807  20180101






### Customers that change status from active to disactive
customer_active_to_diactive_date=customers_first_none_productname_date[customers_first_none_productname_date['CustomerNodeId'].isin(customers_none_active_to_active['CustomerNodeId'])== False]
#[122827 rows x 2 columns]
#        CustomerNodeId  MonthKey
#0              1040415  20181201
#1              1040416  20180601
#3              1040454  20181001
#4              1040471  20190101
#5              1040479  20180301
#               ...       ...
#152566         3086567  20180501
#152595         3086620  20190101
#152644         3086695  20180601
#152664         3086724  20190101
#152673         3086740  20181201






jj=[]
for i,h in zip(customer_active_to_diactive_date['CustomerNodeId'],customer_active_to_diactive_date['MonthKey']):
    jj.append(customers_that_has_none_in_customers_churn_date_of_different_package[(customers_that_has_none_in_customers_churn_date_of_different_package['CustomerNodeId']==i) & (customers_that_has_none_in_customers_churn_date_of_different_package[0]==h)].index[0])
hh=list(map(lambda x:x-1,jj))


customer_active_to_diactive_date['ChurnPackagename']=customers_that_has_none_in_customers_churn_date_of_different_package.loc[hh]['PackageName' ].tolist()



customer_churn_at_packge=customer_active_to_diactive_date.copy()

customer_churn_at_packge.rename(columns={'MonthKey':'ChurnMonthKey'},inplace=True)
customer_churn_at_packge['churn']=[1]*122827
#122827 rows
#        CustomerNodeId  ChurnMonthKey ChurnPackagename  churn
#0              1040415       20181201                P      1
#1              1040416       20180601                I      1
#3              1040454       20181001               IP      1
#4              1040471       20190101               IP      1
#5              1040479       20180301              VIP      1
#               ...            ...              ...    ...
#152566         3086567       20180501                I      1
#152595         3086620       20190101                I      1
#152644         3086695       20180601                I      1
#152664         3086724       20190101                I      1
#152673         3086740       20181201                I      1

#customer_churn_at_packge.to_csv('customer_churn_at_packge.csv',index=False)
### read customer_churn_at_packge those customer active to disactive
customer_churn_at_packge=pd.read_csv('customer_churn_at_packge.csv')



### Explore the MRC of different product name

Product2.columns

Product2[['PackageName','CurrentMRC']].groupby('PackageName').sum()






### some pf thehn when package name is none, but the Current MRC has number
Product2[(Product2['PackageName']=='none') & (Product2['CurrentMRC'].notna())].to_csv('hhhhhh.csv',index=False)

Product2[(Product2['PackageName']=='none') & (Product2['CurrentMRC'].notna())].shape      #（49, 16)

Product2[(Product2['PackageName']=='none') & (Product2['CurrentMRC'].notna())].head(20)
#         CustomerNodeId  MonthKey  ...  CurrentMRC  HasNonStandardRate
#428299          1132391  20191001  ...      140.50                   0
#429924          1132578  20191001  ...      115.50                   0
#444579          1134104  20191001  ...      115.50                   0
#1968519         1421169  20191001  ...      287.25                   0
#2122629         1438793  20191001  ...      140.50                   0
#2507034         1530465  20191001  ...       65.50                   0
#2623722         1541636  20191001  ...       90.50                   0
#2724833         1582596  20191001  ...      115.50                   0
#3724645         1814916  20191001  ...      115.50                   0
#3811018         1822490  20191001  ...       55.00                   0
#3815902         1822876  20191001  ...      348.45                   0
#4104387         1849377  20191001  ...       80.00                   0
#4174347         1854913  20191001  ...      110.45                   0
#4460370         1881304  20191001  ...      115.50                   0
#4482175         1882893  20191001  ...      100.50                   0
#4920829         2009260  20191001  ...       80.00                   0
#5287899         2046888  20191001  ...       80.00                   0
#5356187         2053082  20191001  ...       55.00                   0
#5407471         2058157  20191001  ...       90.50                   0
#5580763         2073911  20191001  ...       65.50                   0


ss=list(Product2['CustomerNodeId'][(Product2['PackageName']=='none') & (Product2['CurrentMRC'].notna())])

Product2[Product2['CustomerNodeId'].isin(ss)].to_csv('jjjjj.csv',index=False)







# %% those customer active to disactive
customer_churn_at_packge=pd.read_csv('customer_churn_at_packge.csv')


customer_churn_at_packge['ChurnPackagename'].value_counts()
#I      87770
#IV     21365
#VIP     7869
#IP      4145
#V       1210
#VP       313
#P        155


#####
Demographic2.columns

Demographic2['SubscriberwiseScore'].value_counts()
Demographic2[['CustomerNodeId','SubscriberwiseScore','CustomerType']].groupby(['CustomerNodeId','SubscriberwiseScore']).count()


# %% Order2

Orders2['DisconnectOrderTypeCount'].value_counts()

Orders2['ChangeOfServiceOrderTypeCount'].value_counts()

ppp=Orders2[Orders2['CustomerNodeId']==2053082]  # 用来查看那些， package name 是none的时候，mRC还是有数字的



