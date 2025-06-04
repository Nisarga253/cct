from flask import Flask, Response
import matplotlib.pyplot as plt
import io
import heapq
from collections import defaultdict
import random

app = Flask(__name__)

@app.route("/")
def stfq_simulation():
    random.seed(0)
    users = ["Alice", "Bob", "Charlie"]
    num_jobs = 15
    jobs = [(random.randint(0, 10), random.randint(1, 5), random.choice(users)) for _ in range(num_jobs)]
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
    plt.figure(figsize=(12, 4))
    for i, (start, end, user, length) in enumerate(schedule):
        plt.barh(user, end - start, left=start, color=colors[user], edgecolor='black')
        plt.text(start + (end - start)/2, users.index(user), f"J{i}", va='center', ha='center', color='white', fontsize=9)
    plt.xlabel("Time")
    plt.title("Start-Time Fair Queuing Simulation")
    plt.grid(axis='x')
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return Response(buf.getvalue(), mimetype='image/png')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
