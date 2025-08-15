#!/bin/bash

# Check that the correct number of arguments are provided
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 regions.txt hic_data.txt output.txt"
    exit 1
fi

regions_file=$1
hic_data_file=$2
output_file=$3  # Output file name from the arguments
aggregated_file=$4  # Name of the aggregated output file

# Clear the output file or create it if it doesn't exist
> "$output_file"
> "$aggregated_file"  # Clear the aggregated file at the start

# Read regions from the regions file
while IFS= read -r line; do
    # Extract the chromosome and coordinates from the line
    chrom=$(echo "$line" | awk '{print $1}')
    start=$(echo "$line" | awk '{print $2}')
    end=$(echo "$line" | awk '{print $3}')

    # Print the command being executed for debugging
    echo "Executing: python3 contact_stats.py \"$hic_data_file\" \"$chrom\" \"$start\" \"$end\""

    # Run the Python script with the extracted variables and append the output
    python3 contact_stats.py "$hic_data_file" "$chrom" "$start" "$end" "$output_file" >> "$output_file" 

    # Append the contents of the output file to the aggregated results file
    cat "$output_file" >> "$aggregated_file"

    # Check if there was an error in the execution of the Python script
    if [ $? -ne 0 ]; then
        echo "An error occurred while executing the Python script for line: $line"
    fi

done < "$regions_file"

echo "Done processing regions."