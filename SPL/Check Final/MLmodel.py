import pandas as pd
import numpy as np,os
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
import joblib

base_path = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_path, "processed_output.csv")
class MLModel:
    def __init__(self, csv_path):
        self.csv_file = csv_path
        self.classifier = None
        self.accuracy = 0
        self.confusion_matrix = None

    def train_model(self):
        try:
            # Load dataset
            df = pd.read_csv(self.csv_file)
            df = df.replace('?', np.nan).dropna()

            # Split dataset
            X = df.drop(columns=['prediction'])
            Y = df['prediction']
            X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

            # Train KNN Classifier
            self.classifier = KNeighborsClassifier(n_neighbors=1, p=2, metric='euclidean')
            self.classifier.fit(X_train, Y_train)

            # Save the trained model
            joblib.dump(self.classifier, 'AppClassifier1.joblib')
            joblib.dump(X_train.columns, 'feature_names.joblib')
            # Test the model
            Y_pred = self.classifier.predict(X_test)
            self.confusion_matrix = confusion_matrix(Y_test, Y_pred)
            self.accuracy = accuracy_score(Y_test, Y_pred)

            return self.accuracy, self.confusion_matrix

        except Exception as e:
            print(f"Error in training the model: {e}")
            return None, None
