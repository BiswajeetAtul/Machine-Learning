#!/usr/bin/env python
# coding: utf-8

# # Telecom Churn
# ## Task:
# ## 1. predict which customers are at high risk of churn.
# ## 2. identify the main indicators of churn.

# Importing all necessary libraries

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('config', 'IPCompleter.greedy=True')
from sklearn.decomposition import IncrementalPCA
from sklearn.decomposition import PCA


# Code to filter unnecessary warnings

# In[2]:


#to Suppress unnecessary warnings
warnings.filterwarnings("ignore")


# Defining the path to the Dataset

# In[3]:


teleDataFile=r'telecom_churn_data.csv'


# Reading the Dataset

# In[4]:


teleData= pd.read_csv(teleDataFile)


# Finding out the number of non-null values in the dataset

# In[5]:


with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(teleData.info(verbose=True,null_counts =True))


# looking into the stats of all the columns of the dataset 

# In[6]:


with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    display(teleData.describe())


# Taking a peek into the dataset

# In[7]:


with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    display(teleData.head(5))


# Finding the number of unique values in each column of the dataset

# In[8]:


with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        display(teleData.nunique(axis=0,dropna=False))


# we can see that there are columns with 1 or 2 unique values to as high as 82k unique values(not taking into account the mobile_number which ofcourse will have unique values) 
# 
# Printing all the unique values for columns with less then 100 unique values including null/nan:

# In[25]:


for col in list(teleData.columns):
    if(teleData[col].nunique()>500 ): continue
    else:
        print(col+":"+str(teleData[col].unique().tolist()))
        print("----------------------------------------------------------------------------------")


# Finding the percentage of Null values in each column:

# In[10]:


with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print (teleData.isnull().mean())


# WE can see that the null values are occuring in pairs. for ex: 
# 
# og_others and ic_others
# 1. og_others_6    --             0.039370 => ic_others_6      --           0.039370
# 2. og_others_7    --             0.038590 => ic_others_7      --           0.038590
# 3. og_others_8    --             0.053781 => ic_others_8      --           0.053781
# 4. og_others_9    --             0.077451 => ic_others_9      --           0.077451
# 
# Same is the case for onnet_mou,offnet_mou,roam_ic_mou,roam_og_mou,loc_og_t2t_mou,loc_og_mou,std_og_t2t_mou,std_og_t2m_mou,std_og_t2f_mou,std_og_t2c_mou,std_og_mou,isd_og_mou,spl_og_mou,og_others,loc_ic_t2t_mou,loc_ic_t2m_mou,loc_ic_t2f_mou,loc_ic_mou,std_ic_t2t_mou etc.
# 
# Infact all these columns are propagating the null value for the same rows. So we can safely put 0 as the missing value for these rows. 

# # Exploratory Data Analysis

# ## Trend and Outlier detection Univariate and Multivariate Analaysis

# In[11]:


fig=plt.figure(figsize=(20,20))

((ax1, ax2), (ax3, ax4)) = fig.subplots(2, 2)

ax1.plot(teleData['offnet_mou_6'],teleData['onnet_mou_6'],"b+")
ax1.set_xlabel("offnet_mou_6")
ax1.set_ylabel("onnet_mou_6")

ax2.plot(teleData['offnet_mou_7'],teleData['onnet_mou_7'],"r+")
ax2.set_xlabel("offnet_mou_7")
ax2.set_ylabel("onnet_mou_7")

ax3.plot(teleData['offnet_mou_8'],teleData['onnet_mou_8'],"g+")
ax3.set_xlabel("offnet_mou_8")
ax3.set_ylabel("onnet_mou_8")

ax4.plot(teleData['offnet_mou_9'],teleData['onnet_mou_9'],"y+")
ax4.set_xlabel("offnet_mou_9")
ax4.set_ylabel("onnet_mou_9")
plt.show()


# In[12]:


fig=plt.figure(figsize=(20,20))

((ax1, ax2), (ax3, ax4)) = fig.subplots(2, 2)

ax1.plot(teleData['og_others_6'],teleData['ic_others_6'],"b+")
ax1.set_xlabel("og_others_6")
ax1.set_ylabel("ic_others_6")

ax2.plot(teleData['og_others_7'],teleData['ic_others_7'],"r+")
ax2.set_xlabel("og_others_7")
ax2.set_ylabel("ic_others_7")

ax3.plot(teleData['og_others_8'],teleData['ic_others_8'],"g+")
ax3.set_xlabel("og_others_8")
ax3.set_ylabel("ic_others_8")

ax4.plot(teleData['og_others_9'],teleData['ic_others_9'],"y+")
ax4.set_xlabel("og_others_9")
ax4.set_ylabel("ic_others_9")
plt.show()


# In[13]:


fig=plt.figure(figsize=(20,20))
((ax1, ax2), (ax3, ax4)) = fig.subplots(2, 2)

ax1.plot(teleData['date_of_last_rech_6'].fillna('6/30/2014'),teleData['onnet_mou_6'],"bo")
ax2.plot(teleData['date_of_last_rech_6'].fillna('6/30/2014'),teleData['offnet_mou_6'],"ro")


ax3.plot(teleData['date_of_last_rech_7'].fillna('7/30/2014'),teleData['onnet_mou_7'],"bo")
ax4.plot(teleData['date_of_last_rech_7'].fillna('7/30/2014'),teleData['offnet_mou_7'],"ro")

plt.show()


# In[14]:


fig=plt.figure(figsize=(20,20))
((ax1, ax2), (ax3, ax4)) = fig.subplots(2, 2)

ax1.plot(teleData['arpu_6'],"bo")
ax2.plot(teleData['arpu_7'],"r+")
ax3.plot(teleData['arpu_8'],"b^")
ax4.plot(teleData['arpu_9'],"r*")

plt.show()


# In[15]:


fig=plt.figure(figsize=(20,20))
((ax1, ax2), (ax3, ax4)) = fig.subplots(2, 2)

ax1.plot(teleData['arpu_3g_6'],"bo")
ax2.plot(teleData['arpu_3g_7'],"r+")
ax3.plot(teleData['arpu_3g_8'],"b^")
ax4.plot(teleData['arpu_3g_9'],"r*")

plt.show()


# In[16]:


fig=plt.figure(figsize=(20,20))
((ax1, ax2), (ax3, ax4)) = fig.subplots(2, 2)

ax1.plot(teleData['arpu_2g_6'],"bo")
ax2.plot(teleData['arpu_2g_7'],"r+")
ax3.plot(teleData['arpu_2g_8'],"b^")
ax4.plot(teleData['arpu_2g_9'],"r*")

plt.show()


# In[17]:


fig=plt.figure(figsize=(20,20))
((ax1, ax2), (ax3, ax4)) = fig.subplots(2, 2)

ax1.plot(teleData['monthly_2g_6'],teleData['vol_2g_mb_6'],"bo")
ax2.plot(teleData['monthly_2g_7'],teleData['vol_2g_mb_7'],"r+")
ax3.plot(teleData['monthly_2g_8'],teleData['vol_2g_mb_8'],"b^")
ax4.plot(teleData['monthly_2g_9'],teleData['vol_2g_mb_9'],"r*")

plt.show()


# In[18]:


fig=plt.figure(figsize=(20,20))
((ax1, ax2), (ax3, ax4)) = fig.subplots(2, 2)

ax1.plot(teleData['monthly_3g_6'],teleData['vol_3g_mb_6'],"bo")
ax2.plot(teleData['monthly_3g_7'],teleData['vol_3g_mb_7'],"r+")
ax3.plot(teleData['monthly_3g_8'],teleData['vol_3g_mb_8'],"b^")
ax4.plot(teleData['monthly_3g_9'],teleData['vol_3g_mb_9'],"r*")

plt.show()


# ## Data Imputation

# All columns where there is 20% missing values:

# In[19]:


colsWith20pnull=pd.Series(  teleData.columns.where(teleData.isnull().mean()<=0.20)).dropna().tolist()
colsWith20pnull


# Imputing values to 0 where the column in not a date type

# In[26]:


cols_noDates=[x for x in teleData.columns if "date" not in x]
teleData_imputed=teleData[cols_noDates].fillna(0)
teleData_imputed.head(10)


# In[27]:


with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print (teleData_imputed.isnull().mean())
display(teleData_imputed.describe())


# We can see that **loc_og_t2o_mou std_og_t2o_mou loc_ic_t2o_mou** have zero as the value, so we can drop them all. same goes for other columns that have only one value

# ## Outlier Treatment

# In[28]:


for col in (teleData_imputed.columns).tolist():
    sns.boxplot(col,data=teleData_imputed,)
    plt.show()


# In[29]:


with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    display(teleData_imputed.describe())


# In[ ]:


sns.pairplot(teleData_imputed)


# We will take care of all outliers during the data preparation after filtering out the high valued customers

# # Data Preperation

# Finding the high values customers:
# 1. Creating a new columns that has average of the revenues of 6th and 7th month
# 2. Finding the 70th percentile and above.
# 3. Filtering the data to get the High Valued customers
# 

# As we can see that all the Average Revenue Columns have no null values, we can proceed forward with finding the Average
# 1. arpu_6        ---              99999 non-null float64
# 2. arpu_7        ---              99999 non-null float64
# 3. arpu_8        ---              99999 non-null float64
# 4. arpu_9        ---              99999 non-null float64

# In[39]:


teleData_imputed['avg_6_7']=(teleData_imputed["total_rech_amt_6"]+teleData_imputed["total_rech_amt_7"]+(teleData_imputed["av_rech_amt_data_6"]*(teleData_imputed["count_rech_3g_6"]+teleData_imputed["count_rech_2g_6"]))+(teleData_imputed["av_rech_amt_data_7"]*(teleData_imputed["count_rech_3g_7"]+teleData_imputed["count_rech_2g_7"])))/


# In[40]:


sns.boxplot(teleData_imputed['avg_6_7'])


# In[41]:


percentile70th= teleData_imputed['avg_6_7'].quantile(0.70)
print("The 70th percentile average revenue is "+ str(percentile70th))


# In[42]:


teleData_HighValuesCustomers= teleData_imputed[teleData_imputed['avg_6_7']>=percentile70th]
teleData_HighValuesCustomers.shape


# Taking a look into the High Valued customers dataset:

# In[43]:


with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    display(teleData_HighValuesCustomers.head(10))


# Now making all Null values 0.

# In[44]:


teleData_HighValuesCustomers_Treated=teleData_HighValuesCustomers.fillna(0)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(teleData_HighValuesCustomers_Treated.info(verbose=True,null_counts =True))


# We can see that all the null values have been treated.
# Thus teleData_HighValuesCustomers_Treated is our dataset that contains the high valued customer with treated data.
# The next step is to tag the numbers as churned(1) and not churned(0)based on the following columns:
# 1. total_ic_mou_9
# 2. total_og_mou_9
# 3. vol_2g_mb_9
# 4. vol_3g_mb_9

# In[45]:


filter=((teleData_HighValuesCustomers_Treated['total_ic_mou_9']==0)&(teleData_HighValuesCustomers_Treated['vol_2g_mb_9']==0)&(teleData_HighValuesCustomers_Treated['vol_3g_mb_9']==0)&(teleData_HighValuesCustomers_Treated['total_og_mou_9']==0))
teleData_HighValuesCustomers_Treated['churned_tag']=np.where(filter, 1, 0)
teleData_HighValuesCustomers_Treated['churned_tag'].sum()


# In[46]:


#filter=((teleData_HighValuesCustomers_Treated['total_ic_mou_9']==0)&(teleData_HighValuesCustomers_Treated['vol_2g_mb_9']==0)&(teleData_HighValuesCustomers_Treated['vol_3g_mb_9']==0)&(teleData_HighValuesCustomers_Treated['total_og_mou_9']==0))
#tagged=teleData_HighValuesCustomers_Treated.ix[filter,list(teleData_HighValuesCustomers_Treated.columns)]
#display(tagged.index)


# In[49]:


with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    display(teleData_HighValuesCustomers_Treated.head(5))


# Now we can see that the rows have a churned indicator against them.
# We can delete all the columns that are related to the churn phase i.e. the '_9' columns
# 
# Removing all columns that have '_9' in them.

# In[50]:


print(len([x for x in teleData_HighValuesCustomers_Treated.columns if '_9' in x]))
print(len(teleData_HighValuesCustomers_Treated.columns))
teleData_HighValuesCustomers_Treated.shape


# In[51]:


colsToDrop=[x for x in teleData_HighValuesCustomers_Treated.columns if '_9' in x]


# In[52]:


teleData_HighValuesCustomers_Tagged=teleData_HighValuesCustomers_Treated.drop(colsToDrop,axis=1)


# In[53]:


teleData_HighValuesCustomers_Tagged.shape


# Now we have removed all the columns that are related to the churn phase.
# Lets have a look at the dataset now.

# In[54]:


with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    display(teleData_HighValuesCustomers_Tagged.head(5))


# We might not need the date columns, so removing them as well.
# 
# creating a new dataset _naDates 

# In[55]:


#teleData_HighValuesCustomers_naDates=teleData_HighValuesCustomers_Tagged.drop([x for x in teleData_HighValuesCustomers_Tagged.columns if 'date' in x],axis=1)
#teleData_HighValuesCustomers_naDates.shape


# In[57]:


#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
 #   display(teleData_HighValuesCustomers_naDates.head(5))


# Now lets see what are the values in the columns, we will not need the columns that have single values so we will drop them

# In[58]:


for col in list(teleData_HighValuesCustomers_Tagged.columns):
    if(teleData_HighValuesCustomers_Tagged[col].nunique()>100 ): continue
    else:
        print(col+":"+str(teleData_HighValuesCustomers_Tagged[col].unique().tolist()))
        print("----------------------------------------------------------------------------------")


# In[59]:


singleValuedColumnsDict={}
for col in list(teleData_HighValuesCustomers_Tagged.columns):
    if(teleData_HighValuesCustomers_Tagged[col].nunique()==1 ):
        singleValuedColumnsDict[col]=teleData_HighValuesCustomers_Tagged[col].unique().tolist()[0]
print(singleValuedColumnsDict)


# Dropping these columns

# In[61]:


teleData_HighValuesCustomers_Final= teleData_HighValuesCustomers_Tagged.drop(list(singleValuedColumnsDict.keys()),axis=1)
teleData_HighValuesCustomers_Final.shape


# Thus here we have taken care of single valued columns, and imputed the missing values. The only thing that remains is outlier treatment. We will also need to remove the mobile number columns or we can make it the index. For the time being we will just drop it.

# In[64]:


teleData_HighValuesCustomers_Final=teleData_HighValuesCustomers_Final.drop('mobile_number',axis=1)


# In[65]:


teleData_HighValuesCustomers_Final.shape


# ## Feature Engineering

# In[ ]:





# In[ ]:





# In[66]:


correlationMatrix=teleData_HighValuesCustomers_Final.corr()


# In[67]:


with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    display(correlationMatrix)


# In[90]:


#print(correlationMatrix.shape)
#help(np.diagonal)
diagonalmatrix=np.diagonal(correlationMatrix)
corr_minus_diag=correlationMatrix-diagonalmatrix
display(corr_minus_diag)


# In[ ]:


plt.figure(figsize=(20, 12))
#plt.subplot(321)
sns.boxplot(x = 'arpu_6', y = 'churned_tag', data = teleData_HighValuesCustomers_Final)
plt.show()


# # PCA

# In[62]:


pca_churn = PCA(0.95)


# In[ ]:


df_train_pca = pca_again.fit_transform(X_train)
df_train_pca.shape

