import os
import joblib
import pandas as pd
import tensorflow as tf

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# ======================================
# PATHS
# ======================================

DATASET = "priority_dataset.csv"

MODEL_DIR = "saved_model"

KERAS_MODEL = "priority_model.keras"

SCALER_FILE = "models/priority_scaler.pkl"


os.makedirs("models", exist_ok=True)


# ======================================
# LOAD DATASET
# ======================================

print("Loading dataset...")

df = pd.read_csv(DATASET)

print(df.head())

print("\nTotal Samples:", len(df))


# ======================================
# FEATURES
# ======================================

X = df[
    [
        "speed",
        "waiting_time",
        "density",
        "acceleration"
    ]
].values


y = df["priority"].values


# ======================================
# TRAIN / TEST
# ======================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# ======================================
# SCALER
# ======================================

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)

X_test = scaler.transform(X_test)

joblib.dump(
    scaler,
    SCALER_FILE
)

print("Scaler saved.")


# ======================================
# MODEL
# ======================================

model = tf.keras.Sequential([

    tf.keras.layers.Input(shape=(4,)),

    tf.keras.layers.Dense(
        32,
        activation="relu"
    ),

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


# ======================================
# TRAIN
# ======================================

print("\nTraining model...\n")

history = model.fit(

    X_train,

    y_train,

    validation_split=0.2,

    epochs=40,

    batch_size=512,

    verbose=1

)


# ======================================
# EVALUATE
# ======================================

loss, mae = model.evaluate(

    X_test,

    y_test,

    verbose=0

)

print("\n==============================")
print("Test MAE :", mae)
print("Test Loss:", loss)
print("==============================")


# ======================================
# SAVE
# ======================================

print("\nSaving models...")

model.save(KERAS_MODEL)

tf.saved_model.save(
    model,
    MODEL_DIR
)

print("SavedModel saved.")

print("Keras model saved.")

print("Scaler saved.")

print("\nDone.")
