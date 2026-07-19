import os
import joblib

from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "priority_model.pkl")
OUTPUT_PATH = os.path.join(BASE_DIR, "models", "priority_model.onnx")

print("Loading trained model...")

model = joblib.load(MODEL_PATH)

print("Converting to ONNX...")

initial_type = [
    ("input", FloatTensorType([None, 4]))
]

onnx_model = convert_sklearn(
    model,
    initial_types=initial_type
)

with open(OUTPUT_PATH, "wb") as f:
    f.write(onnx_model.SerializeToString())

print("\nSUCCESS")
print("Saved:", OUTPUT_PATH)
