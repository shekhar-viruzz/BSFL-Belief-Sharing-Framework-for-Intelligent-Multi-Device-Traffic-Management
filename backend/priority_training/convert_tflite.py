import tensorflow as tf

print("Loading SavedModel...")

converter = tf.lite.TFLiteConverter.from_saved_model(
    "saved_model"
)

print("Converting...")

tflite_model = converter.convert()

with open(
    "priority_model.tflite",
    "wb"
) as f:
    f.write(tflite_model)

print("Done!")

print("Saved priority_model.tflite")
