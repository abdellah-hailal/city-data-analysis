import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt


# Chargement du CSV
df = pd.read_csv("/Users/abdellahhailal/PycharmProjects/Projet_Science/data/villes.csv", quotechar='"', sep=",", engine="python")

# Afficher les premières lignes
print(df.head(10))
print()
print("---------------Étape: 2-----------------")


# Étape 2 : Nettoyage des données

# ---- FONCTION DE NETTOYAGE ----
def nettoyer_villes(df):
    # 1. Supprimer les lignes où des valeurs essentielles manquent
    df = df.dropna(subset=["ville", "pays", "population", "latitude", "longitude"])

    # 2. Garder uniquement les populations positives
    df = df[df["population"] > 0]

    # 3. Filtrer les latitudes et longitudes incorrectes
    df = df[(df["latitude"].between(-90, 90)) &
            (df["longitude"].between(-180, 180))]

    return df

# ---- APPLIQUER LE NETTOYAGE ----
df_clean = nettoyer_villes(df)

# ---- AFFICHER LE RÉSULTAT ----
print("Nombre de lignes AVANT nettoyage :", len(df))
print("Nombre de lignes APRÈS nettoyage :", len(df_clean))
print("Lignes supprimées :", len(df) - len(df_clean))

df_clean.head(20)

print()
print("---------------Étape: 3-----------------")

# Étape 3 : Statistiques descriptives sur la population

stats = df_clean["population"].describe()
pd.options.display.float_format = '{:,.0f}'.format
print(stats)
print()
print("---------------Étape: 4-----------------")


# Étape 4 : Conversion en GeoDataFrame
print()
# Création de la géométrie (longitude, latitude)
geometry = [Point(xy) for xy in zip(df_clean["longitude"], df_clean["latitude"])]

# Création du GeoDataFrame
gdf_villes = gpd.GeoDataFrame(
    df_clean,
    geometry=geometry,
    crs="EPSG:4326"   # Projection WGS84
)

# Afficher les premières lignes
print(gdf_villes.head())

print()
print("---------------Étape: 5-----------------")

# Lire le shapefile sans afficher les multipolygon
pays_gdf = gpd.read_file("/Users/abdellahhailal/PycharmProjects/Projet_Science/data/pays.shp")

# Définir la projection manquante
pays_gdf = pays_gdf.set_crs("EPSG:4326")
print("CRS du shapefile :", pays_gdf.crs)

# Afficher uniquement les colonnes disponibles (sans géométrie)
print("Colonnes du shapefile :")
print(pays_gdf.columns)

print("\nType de géométrie :")
print(pays_gdf.geometry.geom_type.unique())

print("\nSystème de projection CRS :")
print(pays_gdf.crs)

print()
print("---------------Étape: 6-----------------")

# Assurer que les deux GeoDataFrames ont le même CRS
gdf_villes = gdf_villes.to_crs("EPSG:4326")
pays_gdf = pays_gdf.to_crs("EPSG:4326")

# Étape 6 : Jointure spatiale
villes_joint = gpd.sjoin(
    gdf_villes,
    pays_gdf,
    how="left",
    predicate="within"
)

# AFFICHAGE OBLIGATOIRE
print(villes_joint.head(10))

print("\nRésumé des correspondances :")
print("Nombre total de villes :", len(gdf_villes))
print("Nombre de villes avec un pays trouvé :", villes_joint['index_right'].notna().sum())
print("Nombre de villes SANS pays trouvé :", villes_joint['index_right'].isna().sum())

print()
print("---------------Étape: 7-----------------")

# Taille de la figure
plt.figure(figsize=(12, 8))

# Dessiner les pays
pays_gdf.plot(ax=plt.gca(), color="white", edgecolor="black")

# Dessiner les villes, colorées selon la population
villes_joint.plot(
    ax=plt.gca(),
    column="population",
    cmap="viridis",
    markersize=50,
    legend=True
)

plt.title("Carte des villes colorées selon leur population", fontsize=16)
plt.xlabel("Longitude")
plt.ylabel("Latitude")

plt.show()