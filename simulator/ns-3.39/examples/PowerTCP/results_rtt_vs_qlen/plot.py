import matplotlib.pyplot as plt

def plot_rtt_vs_qlen(input_file, output_file="scatter_output.png"):
    x = []
    y = []

    with open(input_file, 'r') as f:
        for line in f:
            tokens = line.split()
            # tokens should look like: ["RTT", "<rtt_value>", "time", "<time_value>", "qlen(0)", "<qlen_value>"]
            if len(tokens) >= 6:
                rtt = float(tokens[1]) / 1000.0
                qlen_kb = float(tokens[5]) / 1024.0
                sport = int(tokens[7])
                if sport == 10000:
                    x.append(qlen_kb)
                    y.append(rtt)

    plt.scatter(x, y, alpha=0.5)
    plt.xlabel("Queue Length (KB)")
    plt.ylabel("RTT (us)")
    plt.title("Node 0 Scatter Plot: RTT vs QueueLength")
    plt.savefig(output_file)  # Save the plot


plot_rtt_vs_qlen("result-powerInt.pkt", "rtt_qlen_scatter.png")
