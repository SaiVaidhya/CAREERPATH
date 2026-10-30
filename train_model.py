"""
CareerPath AI - Model Training Runner Script
Trains the Random Forest and KNN models, evaluates performance,
and outputs model evaluation metrics.
"""

import sys
import os

# Ensure current directory is on PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.ml.data_generator import save_dataset
from app.ml.train import train_and_evaluate

def main():
    print("=" * 60)
    print("    CareerPath AI - ML Pipeline Training & Evaluation")
    print("=" * 60)
    
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))
    dataset_file = os.path.join(data_dir, "careers_dataset.csv")
    model_dir = os.path.join(data_dir, "ml_models")

    print("[1/2] Generating dataset (1500+ records across 15 career classes)...")
    save_dataset(dataset_file)

    print("\n[2/2] Training ML models (Random Forest, KNN) & evaluating metrics...")
    metrics = train_and_evaluate(dataset_file, model_dir)

    print("Pipeline training completed successfully!")
    print(f"Random Forest Accuracy: {metrics['random_forest']['accuracy']}%")
    print(f"KNN Accuracy:           {metrics['knn']['accuracy']}%")

if __name__ == "__main__":
    main()
