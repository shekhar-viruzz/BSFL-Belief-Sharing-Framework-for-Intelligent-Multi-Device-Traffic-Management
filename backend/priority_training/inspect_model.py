import tensorflow as tf

interpreter = tf.lite.Interpreter(
    model_path="priority_model_int8.tflite"
)

interpreter.allocate_tensors()

print("INPUT")
print(interpreter.get_input_details())

print()

print("OUTPUT")
print(interpreter.get_output_details())
