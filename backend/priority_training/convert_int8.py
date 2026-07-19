import tensorflow as tf
import numpy as np
import pandas as pd

print("Loading dataset...")

df = pd.read_csv("priority_dataset.csv")

X = df[
    [
        "speed",
        "waiting_time",
        "density",
        "acceleration"
    ]
].astype(np.float32).values


def representative_dataset():
    for i in range(min(1000, len(X))):
        yield [X[i:i+1]]


print("Loading SavedModel...")

converter = tf.lite.TFLiteConverter.from_saved_model(
    "saved_model"
)

converter.optimizations = [tf.lite.Optimize.DEFAULT]

converter.representative_dataset = representative_dataset

print("Converting INT8...")

tflite_model = converter.convert()

with open(
    "priority_model_int8.tflite",
    "wb"
) as f:
    f.write(tflite_model)

print("Done!")

print("Saved priority_model_int8.tflite")
