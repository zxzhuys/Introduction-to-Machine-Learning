from sklearn.cluster import KMeans
from sklearn import metrics
import numpy as np

print("- Start K-means Clustering -")

line_data = {
    # - Group1: Massive Commuter Lines -
    "Yamanote Line":    [1.1, 4.2], # Average station distance, Millions of passengers
    "Chuo Rapid Line":  [1.5, 3.5],
    
    # - Group2: Inner-city Subways -
    "Ginza Line":       [0.8, 1.1], 
    "Oedo Line":        [0.9, 0.9], 
    "Marunouchi Line":  [0.9, 1.2], 
    
    # - Group3: Long distance Lines -
    "Keiyo Line":       [2.8, 0.4], 
    "Musashino Line":   [3.0, 0.3],
    "Saikyo Line":      [2.6, 0.5]  
}

X = np.array(list(line_data.values()))
line_name = list(line_data.keys())

k = 3 # 3 groups
kmeans_model = KMeans(n_clusters=k, random_state=1)
kmeans_model.fit(X)
labels = kmeans_model.labels_
centers = kmeans_model.cluster_centers_

print("\n- Clustering Completed -")
print(f"3 Groups")

for cluster_id in range(k):
    print(f"\n[Cluster {cluster_id}] (Center: Station Distance - {centers[cluster_id][0]:.1f}km, Passengers - {centers[cluster_id][1]:.1f}million):")
    for i in range(len(labels)):
        if labels[i] == cluster_id:
            print(f"  - {line_name[i]}")

score = metrics.silhouette_score(X, labels)
print(f"\n- Clustering Evaluation -")
print(f"Silhouette Score: {score:.4f}")