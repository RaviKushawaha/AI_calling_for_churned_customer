import pandas as pd

class Preprocessor:
    @staticmethod
    def merge_tables(profile, purchase, support):
        df = (
            profile.merge(purchase, on="customer_id")
                   .merge(support, on="customer_id")
        )
        raw = df[["customer_id","email_id","phone_number"]]  # keep for UI
        df = df.drop(columns=["customer_id","email_id","phone_number"])
        return df, raw

    @staticmethod
    def encode(df, feature_names):
        X = pd.get_dummies(df, drop_first=True)

        for col in feature_names:
            if col not in X.columns:
                X[col] = 0

        return X[feature_names]
