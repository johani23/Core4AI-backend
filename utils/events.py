from typing import List
from fastapi import WebSocket

# قائمة الاتصالات المفتوحة
cluster_events: List[WebSocket] = []

# إرسال رسالة لكل websockets
async def send_cluster_event(message: dict):
    for ws in list(cluster_events):
        try:
            await ws.send_json(message)
        except:
            cluster_events.remove(ws)
