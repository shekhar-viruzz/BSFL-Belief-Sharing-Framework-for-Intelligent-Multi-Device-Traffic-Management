import onnx
from onnxruntime_tools import optimizer

print("Loading model...")

model = optimizer.optimize_model(
    "models/priority_model.onnx"
)

model.save_model_to_file(
    "models/priority_model_optimized.onnx"
)

print("Done.")
