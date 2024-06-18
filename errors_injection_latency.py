import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt

def plot_error_charts(base_dir):
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

    metrics = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    for metric in metrics:
        metric_dir = os.path.join(base_dir, metric)
        errors = [d for d in os.listdir(metric_dir) if os.path.isdir(os.path.join(metric_dir, d))]

        num_errors = len(errors)
        fig, axes = plt.subplots((num_errors + 1) // 2, 2, figsize=(20, 6 * ((num_errors + 1) // 2)), constrained_layout=True)

        if num_errors == 1:
            axes = [axes]

        axes = axes.flatten()

        for ax, error in zip(axes, errors):
            error_dir = os.path.join(metric_dir, error)
            data_file = os.path.join(error_dir, 'data_cleaned.csv')
            if os.path.exists(data_file):
                df = pd.read_csv(data_file)

                for column in df.columns:
                    if column != 'time' and column in syscall_styles:
                        style = syscall_styles[column]
                        ax.plot(df['time'][::3], df[column][::3], label=column, color=style['color'],
                                marker=style['marker'], markersize=8, linewidth=2, linestyle=style['linestyle'])

                ax.set_xlabel('Time(s)', fontsize=18)
                # m = metric.capitalize()
                ax.set_ylabel(f'{metric.capitalize()}(ms)', fontsize=18)
                ax.set_title(f'Error: {error}', fontsize=20)
                ax.grid(True)
                ax.axvline(x=10, color='r', linestyle='--', linewidth=2)  # vertical line at t=10

                ax.set_xlim(left=0)
                ax.set_ylim(bottom=0)
                ax.tick_params(axis='both', which='major', labelsize=18)

        handles, labels = ax.get_legend_handles_labels()
        fig.legend(handles, labels, loc='upper center', ncol=5, fontsize=24, frameon=False, title='Syscalls', title_fontsize=16)

        plt.tight_layout(rect=[0, 0, 1, 0.9])
        plt.savefig(os.path.join(metric_dir, f'{metric}_charts.png'))
        plt.savefig(os.path.join(metric_dir, f'{metric}_charts.svg'))
        plt.close()
        print(f"Charts (PNG and SVG) generated for metric: {metric}")

def main():
    parser = argparse.ArgumentParser(description="Generate multiple charts in one image for each metric type from merged CSV files.")
    parser.add_argument("input_dir", help="Path to the input directory containing the merged CSV files.")
    args = parser.parse_args()

    plot_error_charts(args.input_dir)

if __name__ == "__main__":
    main()

