from sklearn import svm
from sklearn import metrics
import numpy as np

print("- Start -")
X_train = np.array([
    [2.5, 10],  # JR1 Long station distance, Short underground distance
    [3.0, 5],   # JR2 Long, Short
    [0.9, 95],  # Tokyo Metro1 Short, Long
    [1.1, 90],  # Tokyo Metro2 Short, Long
    [1.3, 100], # Toei Subway1 Medium, Almost
    [1.2, 100]  # Toei Subway2 Medium, Almost
])
Y_train = np.array([0, 0, 1, 1, 2, 2]) # JR - 0  Tokyo Metro - 1  Toei Subway - 2

class_names = {
    0: "JR",
    1: "Tokyo Metro",
    2: "Toei Subway"
}
classifier = svm.SVC()
classifier.fit(X_train, Y_train)
print("Train Complete")

X_predict = np.array([
    [2.8, 8],  # Maybe JR
    [0.7, 85],  # Maybe Tokyo Metro
    [1.7, 99],  # Maybe Toei Subway
    [1.6, 90]   # Maybe Toei Subway
])
Y_predict_actual = np.array([0, 1, 2, 2]) 
Y_predict = classifier.predict(X_predict)

print("\n- Prediction Results -")
for i in range(len(X_predict)):
    features = X_predict[i]
    predicted_label = Y_predict[i]
    predicted_class = class_names[predicted_label]
    actual_class = class_names[Y_predict_actual[i]]
    
    print(f"Feature [Station Distance:{features[0]}km, Underground Distance:{features[1]}%] => Predict: {predicted_class} (Actual: {actual_class})")

accuracy = metrics.accuracy_score(Y_predict_actual, Y_predict)

print(f"Accuracy = {accuracy:.2%}")