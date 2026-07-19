import os
import joblib
import pandas as pd
import tensorflow as tf

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# ============================
# Load Dataset
# ============================

print("Loading dataset...")

df = pd.read_csv("priority_dataset.csv")

print(df.head())
print("Samples:", len(df))

# ============================
# Features
# ============================

X = df[
    [
        "speed",
        "waiting_time",
        "density",
        "acceleration"
    ]
]

y = df["priority"]

# ============================
# Train/Test
# ============================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ============================
# Normalize
# ============================

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)

X_test = scaler.transform(X_test)

os.makedirs("models", exist_ok=True)

joblib.dump(
    scaler,
    "models/priority_scaler.pkl"
)

# ============================
# Neural Network
# ============================

model = tf.keras.Sequential([

    tf.keras.layers.Input(shape=(4,)),

    tf.keras.layers.Dense(
        16,
        activation="relu"
    ),

    tf.keras.layers.Dense(
        8,
        activation="relu"
    ),

    tf.keras.layers.Dense(
        1,
        activation="sigmoid"
    )

])

model.compile(

    optimizer="adam",

    loss="mse",

    metrics=["mae"]

)

print("\nTraining...\n")

model.fit(

    X_train,

    y_train,

    validation_split=0.2,

    epochs=30,

    batch_size=256

)

print("\nEvaluating...\n")

loss, mae = model.evaluate(
    X_test,
    y_test
)

print("Loss:", loss)
print("MAE :", mae)

print("\nSaving Keras model...")

model.save("priority_model.keras")

print("Done.")
