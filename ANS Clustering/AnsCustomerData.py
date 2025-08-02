import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from sklearn.decomposition import PCA

# Cargar el dataset
df = pd.read_csv("\Customer Data.csv")
#se dropea/elimina la columna ya que es unico para cada ejemplo del dataset
df = df.drop(columns=['CUST_ID'])
# Echa un vistazo inicial
print(df.isnull().sum())
df = df.dropna()
df['MINIMUM_PAYMENTS'] = df['MINIMUM_PAYMENTS'].fillna(df['MINIMUM_PAYMENTS'].mean())


scaler = StandardScaler()
scaled_data = scaler.fit_transform(df)


inertia = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(scaled_data)
    inertia.append(kmeans.inertia_)

plt.plot(range(1, 11), inertia, marker='o')
plt.xlabel('Numero de clusters')
plt.ylabel('Inercia')
plt.title('Metodo del Codo')
plt.grid()
plt.show()


# cantidad de clusters, cambiar 5 por la cant deseada o luego de ver elbow method
kmeans = KMeans(n_clusters=5, random_state=42)
clusters = kmeans.fit_predict(scaled_data)

# Añadir los clusters al DataFrame original
df['Cluster'] = clusters

# Ver cuantos clientes hay en cada cluster
print(df['Cluster'].value_counts())

# Ver el perfil promedio por cluster
print(df.groupby('Cluster').mean(numeric_only=True))

# metricas de evaluacion
print("Silhouette Score:", silhouette_score(scaled_data, clusters))
print("Davies-Bouldin Index:", davies_bouldin_score(scaled_data, clusters))
print("Calinski-Harabasz Score:", calinski_harabasz_score(scaled_data, clusters))

#test visualizacion de clusteres
# Reducir dimensiones a 2 para graficar
pca = PCA(n_components=2)
pca_components = pca.fit_transform(scaled_data)

# Crea un DataFrame con los componentes principales y los clusters
pca_df = pd.DataFrame(data=pca_components, columns=['PC1', 'PC2'])
pca_df['Cluster'] = clusters

# Graficar
plt.figure(figsize=(10, 6))
for cluster in sorted(df['Cluster'].unique()):
    plt.scatter(pca_df[pca_df['Cluster'] == cluster]['PC1'],
                pca_df[pca_df['Cluster'] == cluster]['PC2'],
                label=f'Cluster {cluster}', alpha=0.6)

plt.title('Visualización de Clusters con PCA (2D)')
plt.xlabel('Componente Principal 1')
plt.ylabel('Componente Principal 2')
plt.legend()
plt.grid(True)
plt.show()