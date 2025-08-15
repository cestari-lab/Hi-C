import pandas as pd
import sys
import os

def read_hic_matrix(filename):
    """Read the Hi-C data matrix file."""
    dataframe = pd.read_csv(
        filename, 
        sep='\t', 
        dtype={'chrom1': str, 'start1': int, 'end1': int, 
               'chrom2': str, 'start2': int, 'end2': int, 
               'count': float},  
        low_memory=False
    )
    return dataframe

def get_region_of_interest(dataframe, chromosome, start, end):
    """Filter based on the specified chromosome and overlapping coordinate range."""
    filtered_data = dataframe[
        (
            (dataframe['chrom1'] == chromosome) & 
            (dataframe['start1'] <= end) &    # start1 is less than or equal to the input end
            (dataframe['end1'] >= start)       # end1 is greater than or equal to the input start
        ) |
        (
            (dataframe['chrom2'] == chromosome) & 
            (dataframe['start2'] <= end) &    # start2 is less than or equal to the input end
            (dataframe['end2'] >= start)       # end2 is greater than or equal to the input start
        )
    ]
    return filtered_data

def main():
    try:
        if len(sys.argv) != 6:
            print("Usage: python script_name.py <hic_file.txt> <chromosome> <start_coord> <end_coord> <output_file.txt>")
            sys.exit(1)

        filepath = sys.argv[1]
        chromosome = sys.argv[2]
        start_coord = int(sys.argv[3])
        end_coord = int(sys.argv[4])
        output_file = sys.argv[5]

        # Reading data
        hic_data = read_hic_matrix(filepath)

        # Print the head of the DataFrame for debugging
        print("Data Preview:")
        print(hic_data.head())

        # Get the region of interest
        region_of_interest = get_region_of_interest(hic_data, chromosome, start_coord, end_coord)

        # Debugging: Print the filtered data
        print("Filtered Data:")
        print(region_of_interest)

        # Output the subset of data for the region of interest to a file
        with open(output_file, 'w') as f:
            f.write(f"# Command: {' '.join(sys.argv)}\n")  # Write the command at the top
            region_of_interest.to_csv(f, sep='\t', index=False, header=True)

        print(f"Filtered data written to {output_file}")

        # Compute statistics for contact counts related to chromosome 1
        stats = region_of_interest.groupby('chrom1')['count'].agg(['sum', 'mean', 'median', 'std']).reset_index()
        stats.columns = ['Chromosome', 'Total Count', 'Mean', 'Median', 'Standard Deviation']

        # Prepare the output filename for statistics
        base_name, ext = os.path.splitext(output_file)
        stats_output_file = f"{base_name}_stats{ext}"

        # Write summary statistics to the new file
        with open(stats_output_file, 'w') as f:
            f.write(f"# Command: {' '.join(sys.argv)}\n")  # Write the command at the top
            stats.to_csv(f, sep='\t', index=False)

        print(f"Statistics written to {stats_output_file}")

        # Check how many records were found
        print(f"Number of matching records: {len(region_of_interest)}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()