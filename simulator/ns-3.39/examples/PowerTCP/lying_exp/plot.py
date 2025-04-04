import matplotlib.pyplot as plt
import bisect

def read_data(filename, t_start, t_end):
    """
    Reads a file and returns lists of time (in seconds) and totalTxByte (in bytes)
    for records between t_start and t_end.
    """
    times = []
    txBytes = []
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split()
            # Create a dictionary from key-value pairs.
            data = {parts[i]: parts[i+1] for i in range(0, len(parts), 2)}
            if 'time' in data and 'totalTxByte' in data:
                t = float(data['time'])
                if t_start <= t <= t_end:
                    times.append(t)
                    txBytes.append(float(data['totalTxByte']))
    return times, txBytes

def extend_to_end(times, values, t_end):
    """
    If the last time is less than t_end, extend the lists by adding t_end with the last value.
    """
    if not times or times[-1] < t_end:
        times.append(t_end)
        values.append(values[-1] if values else 0)
    return times, values

def forward_fill(times, values, t):
    """
    Returns the value at time t using forward-fill:
      - If t is less than the first time, returns the first value.
      - If t is greater than the last time, returns the last value.
      - Otherwise, returns the value corresponding to the greatest time <= t.
    """
    if t <= times[0]:
        return values[0]
    if t >= times[-1]:
        return values[-1]
    i = bisect.bisect_right(times, t) - 1
    return values[i]

def get_forward_filled_values(times, values, common_times):
    return [forward_fill(times, values, t) for t in common_times]

def process_metric(metric, t_start, t_end):
    """
    Processes a given metric (e.g., "powerInt", "hpcc", "powerDelay") by:
      - Reading the prob0 and prob100 files.
      - Extending the data to t_end if necessary.
      - Creating a common timeline.
      - Forward filling values.
      - Converting time (to ms) and txBytes (to KB).
      - Returning the common timeline (in ms) and the computed difference (prob100-prob0 in KB).
    """
    file_prob0 = f"result_burst_prob0/result-{metric}.burst"
    file_prob100 = f"result_burst_prob100/result-{metric}.burst"
    
    times0, txBytes0 = read_data(file_prob0, t_start, t_end)
    times100, txBytes100 = read_data(file_prob100, t_start, t_end)
    
    times0, txBytes0 = extend_to_end(times0, txBytes0, t_end)
    times100, txBytes100 = extend_to_end(times100, txBytes100, t_end)
    
    # Create a common timeline from both files, ensuring t_start and t_end are included.
    common_times = set(times0 + times100)
    common_times.add(t_start)
    common_times.add(t_end)
    common_times = sorted(t for t in common_times if t_start <= t <= t_end)
    
    # Forward fill values for each file on the common timeline.
    values0 = get_forward_filled_values(times0, txBytes0, common_times)
    values100 = get_forward_filled_values(times100, txBytes100, common_times)
    
    # Convert time to ms and txBytes to KB.
    times_ms = [t * 1000 for t in common_times]
    values0_KB = [v / 1e3 for v in values0]
    values100_KB = [v / 1e3 for v in values100]
    
    # Compute difference: (prob100 - prob0)
    diff = [v100 - v0 for v100, v0 in zip(values100_KB, values0_KB)]
    return times_ms, diff

# Define the time range.
t_start = 0.13
t_end = 0.35

# Process each metric.
times_ms_powerInt, diff_powerInt = process_metric("powerInt", t_start, t_end)
times_ms_hpcc, diff_hpcc = process_metric("hpcc", t_start, t_end)
times_ms_powerDelay, diff_powerDelay = process_metric("powerDelay", t_start, t_end)

# Create one figure with all three lines.
plt.figure(figsize=(10, 6))
plt.plot(times_ms_powerInt, diff_powerInt, label="powerInt (Prob100 - Prob0)", marker='o')
plt.plot(times_ms_hpcc, diff_hpcc, label="hpcc (Prob100 - Prob0)", marker='s')
plt.plot(times_ms_powerDelay, diff_powerDelay, label="powerDelay (Prob100 - Prob0)", marker='^')

plt.xlabel("Time (ms)")
plt.ylabel("Difference in Total Tx Byte (KB)")
plt.title("Difference (Prob100 - Prob0) for powerInt, hpcc, and powerDelay")
plt.legend()
plt.grid(True)
plt.tight_layout()

# Save the figure and do not display it.
plt.savefig("plot_all.png")
plt.close()
