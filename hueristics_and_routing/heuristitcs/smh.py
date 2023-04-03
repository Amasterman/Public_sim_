import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt

# Generate a random dataset
np.random.seed(1)
X = np.random.randn(1000, 2)

# Fit the DBSCAN model
dbscan = DBSCAN(eps=0.2, min_samples=5)
dbscan.fit(X)

# Plot the clusters
plt.scatter(X[:,0], X[:,1], c=dbscan.labels_, cmap='rainbow')
plt.show()
