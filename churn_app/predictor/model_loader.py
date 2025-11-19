import joblib

class ModelLoader:
    _model = None
    _features = None

    @classmethod
    def load(cls):
        if cls._model is None:
            cls._model = joblib.load("../churn_ml_model/xgb_churn_model.pkl")
            cls._features = cls._model.get_booster().feature_names
        return cls._model, cls._features
