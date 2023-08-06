from feature_engine.encoding import OneHotEncoder
from feature_engine.imputation import AddMissingIndicator, ArbitraryNumberImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from classification_model.config.core import config

# set up the pipeline
churn_pipe = Pipeline(
    [
        # ===== IMPUTATION =====
        # add missing indicator to numerical variables
        (
            "missing_indicator",
            AddMissingIndicator(variables=config.model_config.numerical_vars_with_na),
        ),
        # impute numerical variables with 0
        (
            "zero_imputation",
            ArbitraryNumberImputer(
                arbitrary_number=0, variables=config.model_config.numerical_vars_with_na
            ),
        ),
        # ===== ENCODING ======
        # encode categorical variables using one hot encoding into k-1 variables
        (
            "categorical_encoder",
            OneHotEncoder(
                drop_last=True, variables=config.model_config.categorical_vars
            ),
        ),
        # ===== SCALING ======
        # scale the training data
        ("scaler", StandardScaler()),
        # ===== PREDICTION ======
        (
            "Logit",
            LogisticRegression(
                C=config.model_config.alpha,
                random_state=config.model_config.random_state,
            ),
        ),
    ]
)
