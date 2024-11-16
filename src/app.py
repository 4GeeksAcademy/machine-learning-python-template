from utils import db_connect
engine = db_connect()

# your code here


# Carga de las librerias de interes
import pandas as pd

# carga de la informacion
data_total = pd.read_csv("https://raw.githubusercontent.com/4GeeksAcademy/data-preprocessing-project-tutorial/main/AB_NYC_2019.csv")

# visualizacion de la data
data_total.head()

# Veamos cual es la dimension de la informacion 
data_total.shape

# Vizualizaremos ahora información sobre los tipos de datos y valores no nulos
data_total.info()

print(f"El número de registros de nombres duplicados es: {data_total['name'].duplicated().sum()}")
print(f"La cantidad de registros de ID de host duplicados es: {data_total['host_id'].duplicated().sum()}")
print(f"El número de registros de identificación duplicados es: {data_total['id'].duplicated().sum()}")

data_total.drop(["id", "name", "host_name", "last_review", "reviews_per_month"], axis = 1, inplace = True)

# visualicemos como quedo la data
data_total.head()

import matplotlib.pyplot as plt 
import seaborn as sns

fig, axis = plt.subplots(2, 3, figsize=(10, 7))

# Creacion del Histograma
sns.histplot(ax = axis[0,0], data = data_total, x = "host_id")
sns.histplot(ax = axis[0,1], data = data_total, x = "neighbourhood_group").set_xticks([])
sns.histplot(ax = axis[0,2], data = data_total, x = "neighbourhood").set_xticks([])
sns.histplot(ax = axis[1,0], data = data_total, x = "room_type")
sns.histplot(ax = axis[1,1], data = data_total, x = "availability_365")
fig.delaxes(axis[1, 2])

# Adjuste del diseño
plt.tight_layout()

# Mostrar el grafico
plt.show()

fig, axis = plt.subplots(4, 2, figsize = (10, 14), gridspec_kw = {"height_ratios": [6, 1, 6, 1]})

sns.histplot(ax = axis[0, 0], data = data_total, x = "price")
sns.boxplot(ax = axis[1, 0], data = data_total, x = "price")

sns.histplot(ax = axis[0, 1], data = data_total, x = "minimum_nights").set_xlim(0, 200)
sns.boxplot(ax = axis[1, 1], data = data_total, x = "minimum_nights")

sns.histplot(ax = axis[2, 0], data = data_total, x = "number_of_reviews")
sns.boxplot(ax = axis[3, 0], data = data_total, x = "number_of_reviews")

sns.histplot(ax = axis[2,1], data = data_total, x = "calculated_host_listings_count")
sns.boxplot(ax = axis[3, 1], data = data_total, x = "calculated_host_listings_count")

# Adjustar el diseño
plt.tight_layout()

# Mostrar el grafico
plt.show()

# Analisis de datos numericos 

# Creamnos un subplot canvas
fig, axis = plt.subplots(4, 2, figsize = (10, 16))

# Creamos un Plates 
sns.regplot(ax = axis[0, 0], data = data_total, x = "minimum_nights", y = "price")

sns.heatmap(data_total[["price", "minimum_nights"]].corr(), annot = True, 
            fmt = ".2f", ax = axis[1, 0], cbar = False)

sns.regplot(ax = axis[0, 1], data = data_total, x = "number_of_reviews", y = "price").set(ylabel = None)

sns.heatmap(data_total[["price", "number_of_reviews"]].corr(), 
            annot = True, fmt = ".2f", ax = axis[1, 1])

sns.regplot(ax = axis[2, 0], data = data_total, 
            x = "calculated_host_listings_count", y = "price").set(ylabel = None)

sns.heatmap(data_total[["price", "calculated_host_listings_count"]].corr(), 
            annot = True, fmt = ".2f", ax = axis[3, 0]).set(ylabel = None)
fig.delaxes(axis[2, 1])
fig.delaxes(axis[3, 1])

# Adjuste del diseño
plt.tight_layout()

# Mostrar el grafico
plt.show()

fig, axis = plt.subplots(figsize = (5, 4))

sns.countplot(data = data_total, x = "room_type", hue = "neighbourhood_group")

# Mostrar el grafico
plt.show()

data_total["room_type"] = pd.factorize(data_total["room_type"])[0]
data_total["neighbourhood_group"] = pd.factorize(data_total["neighbourhood_group"])[0]
data_total["neighbourhood"] = pd.factorize(data_total["neighbourhood"])[0]

fig, axes = plt.subplots(figsize=(15, 15))

sns.heatmap(data_total[["neighbourhood_group", "neighbourhood", "room_type", "price", "minimum_nights",	
                        "number_of_reviews", "calculated_host_listings_count", 
                        "availability_365"]].corr(), annot = True, fmt = ".2f")

# Adjuste del diseño
plt.tight_layout()

# Mostrar el grafico
plt.show()

sns.pairplot(data = data_total)

fig, axes = plt.subplots(3, 3, figsize = (15, 15))

sns.boxplot(ax = axes[0, 0], data = data_total, y = "neighbourhood_group")
sns.boxplot(ax = axes[0, 1], data = data_total, y = "price")
sns.boxplot(ax = axes[0, 2], data = data_total, y = "minimum_nights")
sns.boxplot(ax = axes[1, 0], data = data_total, y = "number_of_reviews")
sns.boxplot(ax = axes[1, 1], data = data_total, y = "calculated_host_listings_count")
sns.boxplot(ax = axes[1, 2], data = data_total, y = "availability_365")
sns.boxplot(ax = axes[2, 0], data = data_total, y = "room_type")

plt.tight_layout()

plt.show()

# Estadisticos (stats) para la variable Price
price_stats = data_total["price"].describe()
price_stats

# Rango intercuratilico (IQR) para la variable Price

price_iqr = price_stats["75%"] - price_stats["25%"]
limite_superior = price_stats["75%"] + 1.5 * price_iqr
limite_inferior = price_stats["25%"] - 1.5 * price_iqr

print(f"Los limites superior e inferior para encontrar valores atipicos son {round(limite_superior, 2)} y {round(limite_inferior, 2)}, con un rango intercuartilico de {round(price_iqr, 2)}")

# Limpieza de los datos atipicos

data_total = data_total[data_total["price"] > 0]

contador_0 = data_total[data_total["price"] == 0].shape[0]
contador_1 = data_total[data_total["price"] == 1].shape[0]

print("Contador de 0: ", contador_0)
print("Contador de 1: ", contador_1)

# Estadisticos (stats) para la variable minimum_nights
nights_stats = data_total["minimum_nights"].describe()
nights_stats

# Rango intercuratilico (IQR) para la variable minimum_nigths

nights_iqr = nights_stats["75%"] - nights_stats["25%"]

limite_superior = nights_stats["75%"] + 1.5 * nights_iqr
limite_inferior = nights_stats["25%"] - 1.5 * nights_iqr

print(f"Los limites superior e inferior para encontrar valores atipicos son {round(limite_superior, 2)} y {round(limite_inferior, 2)}, con un rango intercuartilico de {round(nights_iqr, 2)}")


# Limpieza de los datos atipicos

data_total = data_total[data_total["minimum_nights"] <= 15]

contador_0 = data_total[data_total["minimum_nights"] == 0].shape[0]
contador_1 = data_total[data_total["minimum_nights"] == 1].shape[0]
contador_2 = data_total[data_total["minimum_nights"] == 2].shape[0]
contador_3 = data_total[data_total["minimum_nights"] == 3].shape[0]
contador_4 = data_total[data_total["minimum_nights"] == 4].shape[0]


print("Contador de 0: ", contador_0)
print("Contador de 1: ", contador_1)
print("Contador de 2: ", contador_2)
print("Contador de 3: ", contador_3)
print("Contador de 4: ", contador_4)


# Estadisticas (stats) para la variable number_of_reviews

review_stats = data_total["number_of_reviews"].describe()
review_stats

# Rango intercuratilico (IQR) para la variable number_of_reviews

review_iqr = review_stats["75%"] - review_stats["25%"]

limite_superior = review_stats["75%"] + 1.5 * review_iqr
limite_inferior = review_stats["25%"] - 1.5 * review_iqr

print(f"Los limites superior e inferior para encontrar valores atipicos son {round(limite_superior, 2)} y {round(limite_inferior, 2)}, con un rango intercuartilico de {round(review_iqr, 2)}")


# Estadisticos (stats) de la variable calculated_host_listings_count

hostlist_stats = data_total["calculated_host_listings_count"].describe()
hostlist_stats

# Rango intercuratilico (IQR) para la variable calculated_host_listings_count

hostlist_iqr = hostlist_stats["75%"] - hostlist_stats["25%"]

limite_superior = hostlist_stats["75%"] + 1.5 * hostlist_iqr
limite_inferior = hostlist_stats["25%"] - 1.5 * hostlist_iqr


print(f"Los limites superior e inferior para encontrar valores atipicos son {round(limite_superior, 2)} y {round(limite_inferior, 2)}, con un rango intercuartilico de {round(hostlist_iqr, 2)}")


contador_0 = sum(1 for i in data_total["calculated_host_listings_count"] if i in range(0, 5))
contador_1 = data_total[data_total["calculated_host_listings_count"] == 1].shape[0]
contador_2 = data_total[data_total["calculated_host_listings_count"] == 2].shape[0]

print("Contador de 0: ", contador_0)
print("Contador de 1: ", contador_1)
print("Contador de 2: ", contador_2)

# Limpieza de valores atipicos

data_total = data_total[data_total["calculated_host_listings_count"] > 4]

# Veamos la cantidad de valores faltantes (NaN) en la data

data_total.isnull().sum().sort_values(ascending = False)

from sklearn.preprocessing import MinMaxScaler

num_variables = ["number_of_reviews", "minimum_nights", "calculated_host_listings_count", 
                 "availability_365", "neighbourhood_group", "room_type"]
scaler = MinMaxScaler()
scal_features = scaler.fit_transform(data_total[num_variables])
df_scal = pd.DataFrame(scal_features, index = data_total.index, columns = num_variables)
df_scal["price"] = data_total["price"]
df_scal.head()

from sklearn.feature_selection import chi2, SelectKBest
from sklearn.model_selection import train_test_split

X = df_scal.drop("price", axis = 1)
y = df_scal["price"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)


selection_model = SelectKBest(chi2, k = 4)
selection_model.fit(X_train, y_train)
ix = selection_model.get_support()
X_train_sel = pd.DataFrame(selection_model.transform(X_train), columns = X_train.columns.values[ix])
X_test_sel = pd.DataFrame(selection_model.transform(X_test), columns = X_test.columns.values[ix])

X_train_sel.head()

X_train_sel["price"] = list(y_train)
X_test_sel["price"] = list(y_test)
X_train_sel.to_csv("../data/processed/clean_train.csv", index = False)
X_test_sel.to_csv("../data/processed/clean_test.csv", index = False)


