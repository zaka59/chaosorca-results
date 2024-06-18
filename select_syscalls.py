import pandas as pd
import matplotlib.pyplot as plt

def plot_single_csv(file_path):
    df = pd.read_csv(file_path)

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
            style = syscall_styles[column]
            ax.plot(df['time(s)'][::3], df[column][::3], label=column, color=style['color'],
                    marker=style['marker'], markersize=8, linewidth=2, linestyle=style['linestyle'])

    ax.set_xlabel('Time (s)', fontsize=18)
    ax.set_ylabel('Number of Calls', fontsize=18)
    ax.set_title('Syscall Counts over Time (EINTR on select)', fontsize=20)
    ax.grid(True)
    ax.axvline(x=100, color='r', linestyle='--', linewidth=2)  # vertical line at t=10

    plt.xticks(rotation=45, ha='right')

    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    ax.tick_params(axis='both', which='major', labelsize=18)

    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', ncol=8, fontsize=14, frameon=False, title='Syscalls', title_fontsize=16)

    plt.tight_layout(rect=[0, 0, 1, 0.85])
    plt.savefig('single_chart_fixed.png')
    plt.savefig('single_chart_fixed.svg')
    plt.close()
    print("Charts (PNG and SVG) generated.")

if __name__ == "__main__":
    plot_single_csv('./select:error=EINTR_syscall.csv')

