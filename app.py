import os
from flask import Flask, Response
import matplotlib.pyplot as plt
import io
import random
import heapq
from collections import defaultdict

app = Flask(__name__)

@app.route('/')
def simulate_stfq():
    users = ["Alice", "Bob", "Charlie"]
    num_jobs = 15
    jobs = [
        (random.randint(0, 10), random.randint(1, 5), random.choice(users))
        for _ in range(num_jobs)
    ]
    jobs.sort()

    virtual_time = 0
    last_finish_time = defaultdict(int)
    schedule = []
    heap = []

    def get_start_tag(arrival_time, user):
        return max(virtual_time, last_finish_time[user])

    for arrival_time, length, user in jobs:
        start_tag = get_start_tag(arrival_time, user)
        heapq.heappush(heap, (start_tag, arrival_time, length, user))

    while heap:
        start_tag, arrival_time, length, user = heapq.heappop(heap)
        start_time = max(virtual_time, arrival_time)
        finish_time = start_time + length
        last_finish_time[user] = finish_time
        virtual_time = finish_time
        schedule.append((start_time, finish_time, user, length))

    colors = {"Alice": "red", "Bob": "green", "Charlie": "blue"}
    fig, ax = plt.subplots(figsize=(10, 4))
    for i, (start, end, user, length) in enumerate(schedule):
        ax.barh(user, end - start, left=start, color=colors[user], edgecolor='black')
        ax.text(start + length / 2 - 0.3, ["Alice", "Bob", "Charlie"].index(user),
                f"J{i}", va='center', ha='center', color='white')
    ax.set_xlabel("Time")
    ax.set_title("Start-Time Fair Queuing Simulation")
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return Response(buf.getvalue(), mimetype='image/png')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Get PORT from Render env
    app.run(host="0.0.0.0", port=port)
