import tensorflow as tf


MODEL_PATH = "training/traffic_model.h5"

OUTPUT_PATH = "training/traffic_model.tflite"



# Load model

model = tf.keras.models.load_model(
    MODEL_PATH
)



# Convert

converter = tf.lite.TFLiteConverter.from_keras_model(
    model
)


tflite_model = converter.convert()



# Save

with open(
    OUTPUT_PATH,
    "wb"
) as f:

    f.write(
        tflite_model
    )


print(
    "TFLite model saved:",
    OUTPUT_PATH
)
