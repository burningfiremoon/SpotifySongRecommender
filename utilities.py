import time
from sklearn.cluster import KMeans
import joblib
import boto3

def generate_file_name(model: KMeans, directory: str = "./models") -> str:
    timeStamp = time.strftime("%Y%m%d-%H%M")
    modelName = type(model).__name__
    return f"{directory}/{modelName}_{timeStamp}"


def dump_model(model: KMeans) -> str:
    fileName = generate_file_name(model)
    joblib.dump(model, fileName)
    return fileName


def load_model(directory: str) -> KMeans:
    return joblib.load(directory)

def save_data_frame(song_data, filename="song_data.csv"):
    song_data.to_csv(filename, index=False)
    print(f"Saved file as {filename}")
