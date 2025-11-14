import argparse
import pandas as pd
import os
import joblib
import logging
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def train_model(args):
    logging.info(f"Starting training process with hyperparameters: {args}")

    base_dir = '/opt/ml/input/data'
    train_path = os.path.join(base_dir, args.train_channel, 'train.csv')
    validation_path = os.path.join(base_dir, args.validation_channel, 'validation.csv')
    
    try:
        train_df = pd.read_csv(train_path)
        val_df = pd.read_csv(validation_path)
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return

    X_train = train_df.iloc[:, 1:]
    y_train = train_df.iloc[:, 0]
    X_val = val_df.iloc[:, 1:]
    y_val = val_df.iloc[:, 0]

    model = XGBClassifier(
        n_estimators=args.n_estimators,
        learning_rate=args.learning_rate,
        max_depth=args.max_depth,
        random_state=42,
        use_label_encoder=False,
        eval_metric='logloss'
    )
    
    model.fit(X_train, y_train,
              eval_set=[(X_val, y_val)],
              early_stopping_rounds=args.early_stopping_rounds,
              verbose=False)
    
    logging.info("Model training complete.")

    y_pred = model.predict(X_val)
    accuracy = accuracy_score(y_val, y_pred)
    logging.info(f"Validation Accuracy: {accuracy:.4f}")

    model_output_dir = os.path.join(args.model_dir, 'model.joblib')
    joblib.dump(model, model_output_dir)
    logging.info(f"Model successfully saved to {model_output_dir}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--n-estimators', type=int, default=100)
    parser.add_argument('--learning-rate', type=float, default=0.1)
    parser.add_argument('--max-depth', type=int, default=5)
    parser.add_argument('--early-stopping-rounds', type=int, default=10)
    parser.add_argument('--model-dir', type=str, default=os.environ.get('SM_MODEL_DIR'))
    parser.add_argument('--train-channel', type=str, default='train')
    parser.add_argument('--validation-channel', type=str, default='validation')

    args = parser.parse_args()
    train_model(args)
