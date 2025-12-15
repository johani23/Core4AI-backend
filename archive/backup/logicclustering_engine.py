# logicclustering_engine.py

from sklearn.cluster import KMeans
import numpy as np

# ✅ اجعل هذا السطر في أعلى الملف حتى يكون ظاهرًا عند الاستيراد
user_vectors = {}

def assign_cluster(user_id, answers):
    if not answers or not isinstance(answers, list):
        raise ValueError("Invalid answers format")
    
    try:
        X = list(user_vectors.values()) + [answers]
        X_np = np.array(X)

        if len(set(len(x) for x in X_np)) > 1:
            raise ValueError("All answer vectors must be the same length")

        # ✅ معالجة حالة عدد العينات القليل
        if len(X_np) < 3:
            user_vectors[user_id] = answers
            return 0  # كلهم نفس الكلستر حالياً
        else:
            kmeans = KMeans(n_clusters=3, random_state=0, n_init="auto").fit(X_np)
            cluster_labels = kmeans.labels_
            new_label = int(cluster_labels[-1])
            user_vectors[user_id] = answers
            return new_label

    except Exception as e:
        raise ValueError(f"Clustering failed: {str(e)}")
