import unittest
import pandas as pd

from shapely.geometry import Point

def nettoyer_villes(df):
    df = df.dropna(subset=["ville", "pays", "population", "latitude", "longitude"])
    df = df[df["population"] > 0]
    df = df[(df["latitude"].between(-90, 90)) &
            (df["longitude"].between(-180, 180))]
    return df


class TestDataProcessing(unittest.TestCase):

    def test_nettoyage_enleve_nan(self):
        df = pd.DataFrame({
            "ville": ["A", None],
            "pays": ["X", "Y"],
            "population": [1000, 2000],
            "latitude": [40, 10],
            "longitude": [-70, -90]
        })
        result = nettoyer_villes(df)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["ville"], "A")

    def test_population_positive(self):
        df = pd.DataFrame({
            "ville": ["A", "B"],
            "pays": ["X", "Y"],
            "population": [1000, -50],
            "latitude": [40, 10],
            "longitude": [-70, -90]
        })
        result = nettoyer_villes(df)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["population"], 1000)

    def test_coordonnees_valides(self):
        df = pd.DataFrame({
            "ville": ["A", "B"],
            "pays": ["X", "Y"],
            "population": [1000, 2000],
            "latitude": [45, 999],   # 999 invalide
            "longitude": [-70, -90]
        })
        result = nettoyer_villes(df)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["latitude"], 45)

    def test_stats(self):
        df = pd.DataFrame({"population": [1000, 2000, 3000]})
        stats = df["population"].describe()
        self.assertEqual(stats["mean"], 2000)
        self.assertEqual(stats["min"], 1000)
        self.assertEqual(stats["max"], 3000)


if __name__ == '__main__':
    unittest.main()
