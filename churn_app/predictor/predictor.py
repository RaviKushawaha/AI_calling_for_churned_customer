import pandas as pd
from .model_loader import ModelLoader
from .preprocessor import Preprocessor

class ChurnPredictor:
    def __init__(self):
        self.model, self.features = ModelLoader.load()

    def predict_top_k(self, profile, purchase, support, k=0.1):
        df, raw_info = Preprocessor.merge_tables(profile, purchase, support)
        X = Preprocessor.encode(df, self.features)

        probs = self.model.predict_proba(X)[:, 1]
        raw_info["prob"] = probs

        top_n = int(len(raw_info) * k)
        return raw_info.sort_values("prob", ascending=False).head(top_n)
