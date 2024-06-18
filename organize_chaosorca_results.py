import os
import shutil
import argparse
import pandas as pd

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def organize_files(base_dir, destination_dir):
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.csv'):
                parts = file.split(':')
                if len(parts) > 1:
                    syscall_info = parts[0]
                    error_and_metric = parts[1].split('_')
                    error_info = None
                    metric_type = None
                    for part in error_and_metric:
                        if part.startswith('error='):
                            error_info = part.split('=')[1]
                        if part.endswith('.csv'):
                            metric_type = part.replace('.csv', '')

                    if metric_type and error_info:
                        metric_dir = os.path.join(destination_dir, metric_type)
                        error_dir = os.path.join(metric_dir, error_info)
                        create_dir(error_dir)

                        src_file = os.path.join(root, file)
                        dst_file = os.path.join(error_dir, file)
                        shutil.move(src_file, dst_file)

def merge_csv_files(base_dir):
    for root, dirs, files in os.walk(base_dir):
        for dir in dirs:
            error_dir = os.path.join(root, dir)
            csv_files = [f for f in os.listdir(error_dir) if f.endswith('.csv')]
            if csv_files:
                merged_df = pd.DataFrame()
                for csv_file in csv_files:
                    syscall = csv_file.split(':')[0]
                    csv_path = os.path.join(error_dir, csv_file)
                    df = pd.read_csv(csv_path)
                    if df.shape[1] > 1:  # Ensure there are at least two columns to avoid errors
                        merged_df[syscall] = df.iloc[:, 1]  # Ignore the first column (timestamp) and take the second column

                if not merged_df.empty:
                    merged_df['time'] = [i * 0.5 for i in range(len(merged_df))]
                    merged_df = merged_df[['time'] + [col for col in merged_df.columns if col != 'time']]
                    merged_df.to_csv(os.path.join(error_dir, 'data.csv'), index=False)
                    print(f"data.csv created for {dir}")

def main():
    parser = argparse.ArgumentParser(description="Organize CSV files by metric type and error and merge them.")
    parser.add_argument("input_dir", help="Path to the input directory containing the CSV files.")
    parser.add_argument("output_dir", help="Path to the output directory where files will be organized and merged.")
    args = parser.parse_args()

    organize_files(args.input_dir, args.output_dir)
    merge_csv_files(args.output_dir)

if __name__ == "__main__":
    main()
