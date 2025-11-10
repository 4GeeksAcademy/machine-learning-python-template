from utils import db_connect
engine = db_connect()

# your code here

# Step 0: Import Libraries and modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#Herramienta de Machine Learning
from sklearn.model_selection import train_test_split

# Step 1: Load data
url='https://breathecode.herokuapp.com/asset/internal-link?id=927&path=AB_NYC_2019.csv'
df_raw = pd.read_csv(url)

df_raw.sample(10, random_state=2025)

# Step 2: Reprocessing
df_baking = df_raw.copy()
df_baking = df_baking.drop(columns=['id','name', 'host_name', 'last_review', 'reviews_per_month','latitude','longitude'])
columnsCategory = ['host_id','neighbourhood_group','neighbourhood','room_type']
df_baking[columnsCategory] = df_baking[columnsCategory].astype('category')
df = df_baking.copy()
df.info()
df_raw.sample(5, random_state=2025)

# Step 3: EDA
df_train, df_test =  train_test_split(df, test_size=0.1, random_state= 2025)
df_train = df_train.reset_index(drop=True)
df_test = df_test.reset_index(drop=True)

df_train.shape, df_test.shape

display(df_train.describe(include = 'number').T)
display(df_train.describe(include = 'category').T)

#Análisis univariado
df_train.hist()
plt.tight_layout()
plt.show()

sns.countplot(data= df_train, x='host_id')
plt.show()

sns.countplot(data= df_train, x='neighbourhood_group')
plt.show()

sns.countplot(data= df_train, x='neighbourhood')
plt.show()

sns.countplot(data= df_train, x='room_type')
plt.show()

#Análisis bivariado para datos númericos
sns.pairplot(data = df_train, corner= True)
plt.show()

#comparamos numericos contra categoricos
sns.pairplot(df_train, hue='neighbourhood_group', corner=True)
plt.show()

#Comparamos categorico contra cateogtrico
sns.countplot(df_train, x = "room_type", hue = "neighbourhood_group")
plt.show()