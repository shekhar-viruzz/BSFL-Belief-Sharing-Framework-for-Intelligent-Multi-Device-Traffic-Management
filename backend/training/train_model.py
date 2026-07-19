import pandas as pd
import tensorflow as tf
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler



DATASET = "training/traffic_dataset.csv"

MODEL_OUTPUT = "training/traffic_model.h5"

SCALER_OUTPUT = "training/scaler.pkl"



# Load dataset

data = pd.read_csv(DATASET)



print(data.head())



# Features

X = data[
    [
        "speed",
        "waiting_time",
        "density",
        "acceleration"
    ]
]



# Labels

encoder = LabelEncoder()


y = encoder.fit_transform(

    data["label"]

)


print(
    "Classes:",
    encoder.classes_
)



# Normalize input

scaler = StandardScaler()


X = scaler.fit_transform(X)



# Save scaler

joblib.dump(

    scaler,

    SCALER_OUTPUT

)


print(
    "Scaler saved:",
    SCALER_OUTPUT
)



# Split dataset

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.2,

    random_state=42

)



# Neural Network

model = tf.keras.Sequential([


    tf.keras.layers.Dense(

        32,

        activation="relu",

        input_shape=(4,)

    ),


    tf.keras.layers.Dense(

        16,

        activation="relu"

    ),


    tf.keras.layers.Dense(

        3,

        activation="softmax"

    )

])



model.compile(

    optimizer="adam",

    loss="sparse_categorical_crossentropy",

    metrics=["accuracy"]

)



model.summary()



# Training

model.fit(

    X_train,

    y_train,

    epochs=50,

    batch_size=32,

    validation_data=(

        X_test,

        y_test

    )

)



# Evaluation

loss, accuracy = model.evaluate(

    X_test,

    y_test

)


print(
    "Accuracy:",
    accuracy
)



# Save model

model.save(

    MODEL_OUTPUT

)


print(

    "Model saved:",

    MODEL_OUTPUT

)
