import datetime
from collections import defaultdict

# عداد النشاط لكل Cluster
activity_counter = {}
activity_log = defaultdict(list)
idle_cycles_per_cluster = {}

def log_activity(cluster_name: str):
    now = datetime.datetime.utcnow()
    activity_log[cluster_name].append(now)
    # احتفظ بالسجلات لآخر ساعة فقط
    activity_log[cluster_name] = [
        ts for ts in activity_log[cluster_name] if (now - ts).seconds <= 3600
    ]
