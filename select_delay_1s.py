import pandas as pd
import matplotlib.pyplot as plt

def plot_single_csv(file_path, title, output_file):
    df = pd.read_csv(file_path)

    if pd.to_datetime(df['timestamp']).iloc[0] > pd.to_datetime(df['timestamp']).iloc[-1]:
        df = df.iloc[::-1].reset_index(drop=True)

    # Convert the timestamps to seconds
    df['time(s)'] = pd.to_datetime(df['timestamp']).astype(int) / 10**9
    df['time(s)'] -= df['time(s)'].min()  # Normalize to start from 0

    syscall_styles = {
        'readv': {'color': 'b', 'marker': 'o', 'linestyle': '-'},
        'open': {'color': 'g', 'marker': 's', 'linestyle': '--'},
        'read': {'color': 'r', 'marker': 'D', 'linestyle': '-.'},
        'select': {'color': 'c', 'marker': '^', 'linestyle': ':'},
        'writev': {'color': 'm', 'marker': 'v', 'linestyle': '-'},
        'sendfile64': {'color': 'y', 'marker': '<', 'linestyle': '--'},
        'write': {'color': 'k', 'marker': '>', 'linestyle': '-.'},
        'poll': {'color': 'orange', 'marker': 'p', 'linestyle': ':'},
        'sendfile': {'color': 'purple', 'marker': 'h', 'linestyle': '-'}
    }

    colors = plt.cm.tab20.colors
    markers = ['o', 's', 'D', '^', 'v', '<', '>', 'p', 'h', '*', 'X', 'P']
    linestyles = ['-', '--', '-.', ':']

    current_styles = len(syscall_styles)
    for i, column in enumerate(df.columns):
        if column not in ['timestamp', 'time(s)'] and column not in syscall_styles:
            syscall_styles[column] = {
                'color': colors[(current_styles + i) % len(colors)],
                'marker': markers[(current_styles + i) % len(markers)],
                'linestyle': linestyles[(current_styles + i) % len(linestyles)]
            }

    fig, ax = plt.subplots(figsize=(20, 12))

    for column in df.columns:
        if column not in ['timestamp', 'time(s)']:
            style = syscall_styles['select']
            ax.plot(df['time(s)'][::3], df[column][::3], label=column, color=style['color'],
                    marker=style['marker'], markersize=10, linewidth=5, linestyle=style['linestyle'])

    ax.set_xlabel('Time (s)', fontsize=18)
    ax.set_ylabel('Latency (ms)', fontsize=18)
    ax.set_title(title, fontsize=24)
    ax.grid(True)
    ax.axvline(x=100, color='r', linestyle='--', linewidth=5)  # vertical line at t=50
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    ax.tick_params(axis='both', which='major', labelsize=18)

    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, ['select'], loc='upper center', ncol=8, fontsize=18, frameon=False, title='Syscalls', title_fontsize=16)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(output_file)
    plt.savefig(output_file.replace('.png', '.svg'))
    plt.close()
    print(f"Charts (PNG and SVG) generated and saved as {output_file}.")

if __name__ == "__main__":
    plot_single_csv('./select:delay_enter=1000000_latency.csv', 'Syscall select on latency with 1s Delay', 'latency_1s_delay.png')

