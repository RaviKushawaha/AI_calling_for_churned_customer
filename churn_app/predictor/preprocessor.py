import pandas as pd

class Preprocessor:
    @staticmethod
    def merge_tables(profile, purchase, support):
        df = (
            profile.merge(purchase, on="customer_id")
                   .merge(support, on="customer_id")
        )

        # need these for UI (raw_info)
        raw = df[[
            "customer_id",
            "email_id",
            "phone_number",
            "avg_order_value",
            "acquisition_channel",
            "days_since_last_purchase",
        ]].copy()

        df = df.drop(columns=["customer_id","email_id","phone_number"])
        
        return df, raw

    @staticmethod
    def encode(df, feature_names):
        X = pd.get_dummies(df, drop_first=True)

        for col in feature_names:
            if col not in X.columns:
                X[col] = 0

        return X[feature_names]
