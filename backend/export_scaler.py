import joblib

scaler = joblib.load("scaler.pkl")

print("MEAN")
print(scaler.mean_)

print("\nSCALE")
print(scaler.scale_)
