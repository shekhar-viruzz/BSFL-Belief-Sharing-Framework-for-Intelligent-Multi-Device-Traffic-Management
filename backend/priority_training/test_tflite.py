import tensorflow as tf
import numpy as np

print("Loading TFLite model...")

interpreter = tf.lite.Interpreter(
    model_path="priority_model_int8.tflite"
)

interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print("Input:", input_details)
print("Output:", output_details)

# Example vehicle:
# speed, waiting_time, density, acceleration
sample = np.array([[5.0, 15.0, 40.0, -1.5]], dtype=np.float32)

# Quantize input if required
if input_details[0]["dtype"] == np.int8:
    scale, zero_point = input_details[0]["quantization"]
    sample = sample / scale + zero_point
    sample = sample.astype(np.int8)

interpreter.set_tensor(input_details[0]["index"], sample)
interpreter.invoke()

prediction = interpreter.get_tensor(output_details[0]["index"])

# Dequantize output if required
if output_details[0]["dtype"] == np.int8:
    scale, zero_point = output_details[0]["quantization"]
    prediction = (prediction.astype(np.float32) - zero_point) * scale

print("\nPriority Score:", prediction[0][0])
