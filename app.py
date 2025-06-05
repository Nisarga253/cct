from flask import Flask, Response
import matplotlib.pyplot as plt
import io
import random
import heapq
from collections import defaultdict

app = Flask(__name__)

@app.route('/')
def simulate_stfq():
    # Step 1: Generate random jobs
    users = ["Alice", "Bob", "Charlie"]
    num_jobs = 15
    jobs = [
        (random.randint(0, 10), random.randint(1, 5), random.choice(users))
        for _ in range(num_jobs)
    ]
    jobs.sort()  # Sort by arrival time

    # Step 2: Initialize ST-FQ variables
    virtual_time = 0
    last_finish_time = defaultdict(int)
    schedule = []
    heap = []  # (start_tag, arrival_time, length, user)

    def get_start_tag(arrival_time, user):
        return max(virtual_time, last_finish_time[user])

    # Step 3: Push all jobs to the heap
    for arrival_time, length, user in jobs:
        start_tag = get_start_tag(arrival_time, user)
        heapq.heappush(heap, (start_tag, arrival_time, length, user))

    # Step 4: Schedule jobs in ST-FQ order
    while heap:
        start_tag, arrival_time, length, user = heapq.heappop(heap)
        start_time = max(virtual_time, arrival_time)
        finish_time = start_time + length
        last_finish_time[user] = finish_time
        virtual_time = finish_time
        schedule.append((start_time, finish_time, user, length))

    # Step 5: Plotting
    colors = {"Alice": "red", "Bob": "green", "Charlie": "blue"}
    fig, ax = plt.subplots(figsize=(10, 4))
    for i, (start, end, user, length) in enumerate(schedule):
        ax.barh(user, end - start, left=start, color=colors[user], edgecolor='black')
        ax.text(start + length / 2 - 0.3, users.index(user), f"J{i}", va='center', ha='center', color='white')
    ax.set_xlabel("Time")
    ax.set_title("Start-Time Fair Queuing Simulation")
    plt.tight_layout()

    # Step 6: Return plot as HTTP response
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return Response(buf.getvalue(), mimetype='image/png')

