import tensorflow as tf
import numpy as np


MODEL_PATH = "training/traffic_model.tflite"


# Load model

interpreter = tf.lite.Interpreter(
    model_path=MODEL_PATH
)

interpreter.allocate_tensors()



input_details = interpreter.get_input_details()

output_details = interpreter.get_output_details()



print("\nINPUT DETAILS")
print(input_details)


print("\nOUTPUT DETAILS")
print(output_details)



# Test cases

tests = [

    # Congestion
    [
        1.0,
        20.0,
        50,
        -2.0
    ],


    # Slow traffic
    [
        4.5,
        5.0,
        20,
        -0.5
    ],


    # Normal
    [
        13.0,
        0.0,
        5,
        0.2
    ]

]



classes = [

    "CONGESTION",

    "NORMAL",

    "SLOW_TRAFFIC"

]



for data in tests:


    input_data = np.array(
        [data],
        dtype=np.float32
    )


    interpreter.set_tensor(

        input_details[0]["index"],

        input_data

    )


    interpreter.invoke()


    output = interpreter.get_tensor(

        output_details[0]["index"]

    )


    result = classes[
        np.argmax(output)
    ]


    confidence = np.max(output)



    print("\nInput:")
    print(data)


    print(
        "Prediction:",
        result
    )


    print(
        "Confidence:",
        confidence
    )
