import tensorflow as tf

print("Loading Keras model...")

model = tf.keras.models.load_model("priority_model.keras")

print("Exporting SavedModel...")

model.export("saved_model")

print("Done!")
print("SavedModel created.")
