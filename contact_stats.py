import sys
import numpy as np

def read_hic_matrix(filename):
    """Read the Hi-C data matrix file and return a list of interactions."""
    data = []
    with open(filename, 'r') as file:
        header = file.readline()  # Skip the header line
        for line in file:
            parts = line.strip().split('\t')  # Assuming tab-separated values
            if len(parts) == 7:  # Ensure there are 7 columns
                try:
                    data.append({
                        'chrom1': parts[0],
                        'start1': int(parts[1]),
                        'end1': int(parts[2]),
                        'chrom2': parts[3],
                        'start2': int(parts[4]),
                        'end2': int(parts[5]),
                        'count': float(parts[6])
                    })
                except ValueError as e:
                    print(f"Error processing line: {line.strip()}. {e}")
                    continue  # Skip problematic line
    return data

def calculate_statistics(data, target_chromosome, target_start, target_end):
    """Calculate statistics for the specified chromosome within the given coordinates."""
    filtered_data = [
        contact for contact in data
        if contact['chrom1'] == target_chromosome and
           contact['start1'] >= target_start and
           contact['end1'] <= target_end
    ]

    if not filtered_data:
        print("No matching contacts found for the specified chromosome and coordinates.")
        return None

    contact_counts = [contact['count'] for contact in filtered_data]
    total_count = sum(contact_counts)
    mean_count = np.mean(contact_counts)
    median_count = np.median(contact_counts)
    std_dev_count = np.std(contact_counts)

    return total_count, mean_count, median_count, std_dev_count

def main():
    try:
        if len(sys.argv) != 6:
            print("Usage: python contact_stats.py <hic_file.txt> <chromosome> <start_coord> <end_coord> <output_file.txt>")
            sys.exit(1)

        filepath = sys.argv[1]
        target_chromosome = sys.argv[2]
        target_start = int(sys.argv[3])
        target_end = int(sys.argv[4])
        output_file = sys.argv[5]

        # Read the Hi-C data
        hic_data = read_hic_matrix(filepath)

        # Calculate statistics for the given chromosome and coordinates
        stats = calculate_statistics(hic_data, target_chromosome, target_start, target_end)

        if stats is not None:
            total_count, mean_count, median_count, std_dev_count = stats

            # Prepare summary output
            with open(output_file, 'w') as f:
                f.write("Chromosome\tTotal Count\tMean\tMedian\tStandard Deviation\n")
                f.write(f"{target_chromosome}\t{total_count}\t{mean_count:.2f}\t{median_count:.2f}\t{std_dev_count:.2f}\n")

            print(f"Statistics written to {output_file}")

    except ValueError as ve:
        print(f"Value Error: {ve}. Ensure you provide valid integer coordinates.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()