import os
import matplotlib.pyplot as plt

def parse_file(filename):
    """
    Reads a file line-by-line and extracts time (s), throughput (bits/s), and qlen (bytes).
    Returns lists of times (ms, shifted so 0.149s => 0ms), throughputs (Gbps), and qlens (KB),
    *only* for times between 0.149s and 0.154s.
    """
    times_ms = []
    throughputs_gbps = []
    qlens_kb = []
    
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 2:
                continue  # skip malformed lines

            # Convert each pair (key, value) into a dictionary
            data = {}
            for i in range(0, len(parts), 2):
                key = parts[i]
                val = float(parts[i+1])
                data[key] = val
            
            # Only include lines where time is between 0.149 and 0.154 seconds
            t_s = data.get('time', 0)
            if 0.149 <= t_s <= 0.154:
                # Normalize time so that 0.149s -> 0ms and 0.154s -> 5ms
                t_ms = (t_s - 0.149) * 1000.0

                # Convert throughput from bits/s to Gbps
                tput_gbps = data['throughput'] / 1e9

                # Convert qlen from bytes to KB
                qlen_kb = data['qlen'] / 1024.0
                
                times_ms.append(t_ms)
                throughputs_gbps.append(tput_gbps)
                qlens_kb.append(qlen_kb)
    
    return times_ms, throughputs_gbps, qlens_kb

def plot_burst_file(filename):
    times_ms, throughputs_gbps, qlens_kb = parse_file(filename)
    
    if not times_ms:
        print(f"No data in [0.149s, 0.154s] for {filename}. Skipping plot.")
        return
    
    # Sort by normalized time for a clean line plot
    combined = sorted(zip(times_ms, throughputs_gbps, qlens_kb), key=lambda x: x[0])
    times_ms, throughputs_gbps, qlens_kb = zip(*combined)
    
    plt.figure()
    ax1 = plt.gca()  # primary axis
    
    # Plot throughput (Gbps) on the left axis
    ax1.plot(times_ms, throughputs_gbps, color='blue', label='Throughput (Gbps)')
    ax1.set_xlabel('Time (ms) [0.149s => 0ms, 0.154s => 5ms]')
    ax1.set_ylabel('Throughput (Gbps)', color='blue')
    ax1.set_ylim([0, 30])         # y-axis from 0 to 30 Gbps
    ax1.set_xlim([0, 5])          # x-axis from 0 to 5 ms (normalized)
    
    # Create a secondary y-axis for qlen (KB)
    ax2 = ax1.twinx()
    ax2.plot(times_ms, qlens_kb, color='red', label='Qlen (KB)')
    ax2.set_ylabel('Qlen (KB)', color='red')
    ax2.set_ylim([0, 2000])       # y-axis from 0 to 2000 KB
    
    # Combine legend
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    plt.legend(lines_1 + lines_2, labels_1 + labels_2, loc='best')
    
    plt.title(f'Throughput & Qlen vs. Time (Normalized)\n{filename}')
    
    return plt

def main():
    # Files to process
    burst_files = [
        "result-powerInt.burst",
        "result-powerDelay.burst",
        "result-timely.burst",
    ]
    
    # Create "figures" directory if it doesn't exist
    os.makedirs("figures", exist_ok=True)
    
    for filename in burst_files:
        if not os.path.isfile(filename):
            print(f"File not found: {filename}, skipping.")
            continue
        
        plt_obj = plot_burst_file(filename)
        if plt_obj:
            # Derive PNG filename in "figures" folder
            base_name = os.path.splitext(os.path.basename(filename))[0]
            out_png = os.path.join("figures", f"{base_name}_normalized_0_5ms.png")
            
            plt_obj.savefig(out_png)
            plt_obj.close()
            print(f"Saved plot to {out_png}")

if __name__ == "__main__":
    main()
