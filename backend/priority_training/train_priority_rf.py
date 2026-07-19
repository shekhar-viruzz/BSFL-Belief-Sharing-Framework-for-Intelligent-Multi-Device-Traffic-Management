import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score


# ===========================
# Paths
# ===========================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATASET = os.path.join(
    BASE_DIR,
    "training",
    "priority_dataset.csv"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "priority_training",
    "models"
)

os.makedirs(MODEL_DIR, exist_ok=True)


# ===========================
# Load Dataset
# ===========================

print("Loading dataset...")
df = pd.read_csv(DATASET)

print(df.head())
print()

print("Total Samples:", len(df))
print()


# ===========================
# Features
# ===========================

X = df[
    [
        "speed",
        "waiting_time",
        "density",
        "acceleration"
    ]
]

y = df["priority"]


# ===========================
# Train/Test Split
# ===========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# ===========================
# Standardize
# ===========================

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)

X_test = scaler.transform(X_test)


# ===========================
# Train Model
# ===========================

print("Training Priority Model...\n")

model = RandomForestRegressor(

    n_estimators=100,

    random_state=42,

    n_jobs=-1

)

model.fit(

    X_train,

    y_train

)


# ===========================
# Evaluate
# ===========================

prediction = model.predict(X_test)

mae = mean_absolute_error(

    y_test,

    prediction

)

r2 = r2_score(

    y_test,

    prediction

)

print("--------------------------------")

print("Mean Absolute Error :", mae)

print("R2 Score            :", r2)

print("--------------------------------")


# ===========================
# Feature Importance
# ===========================

print("\nFeature Importance\n")

for feature, importance in zip(

    X.columns,

    model.feature_importances_

):

    print(

        feature,

        ":",

        round(importance, 4)

    )


# ===========================
# Save Model
# ===========================

joblib.dump(

    model,

    os.path.join(

        MODEL_DIR,

        "priority_model.pkl"

    )

)

joblib.dump(

    scaler,

    os.path.join(

        MODEL_DIR,

        "priority_scaler.pkl"

    )

)

print("\nPriority model saved.")

print("Scaler saved.")

print()

print("Location:")

print(MODEL_DIR)
