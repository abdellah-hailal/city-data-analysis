import unittest
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point


def convertir_en_geodf(df):
    geometry = [Point(xy) for xy in zip(df["longitude"], df["latitude"])]
    return gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")


class TestGeoProcessing(unittest.TestCase):

    def test_conversion_geodf(self):
        df = pd.DataFrame({
            "ville": ["A"],
            "pays": ["B"],
            "population": [1000],
            "latitude": [45],
            "longitude": [-73]
        })
        gdf = convertir_en_geodf(df)

        self.assertIn("geometry", gdf.columns)
        self.assertEqual(gdf.crs.to_string(), "EPSG:4326")
        self.assertEqual(gdf.geometry.iloc[0].x, -73)
        self.assertEqual(gdf.geometry.iloc[0].y, 45)

    def test_jointure_spatiale(self):
        df = pd.DataFrame({
            "ville": ["A"],
            "pays": ["B"],
            "population": [1000],
            "latitude": [45],
            "longitude": [-73]
        })

        villes = convertir_en_geodf(df)
        pays = gpd.read_file("/Users/abdellahhailal/Downloads/pays.shp").set_crs("EPSG:4326")

        result = gpd.sjoin(villes, pays, how="left", predicate="within")

        self.assertIn("index_right", result.columns)


if __name__ == '__main__':
    unittest.main()
