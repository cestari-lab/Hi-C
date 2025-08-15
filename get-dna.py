import sys
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

def extract_sequence(fasta_file, chromosome, start, end):
    for record in SeqIO.parse(fasta_file, "fasta"):
        if record.id == chromosome:
            sequence = record.seq[start-1:end]
            return sequence
    return None

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python extract_dna.py <fasta_path> <chromosome> <start> <end> <output_fasta>")
        sys.exit(1)

    fasta_path = sys.argv[1]
    chromosome = sys.argv[2]
    start = int(sys.argv[3])
    end = int(sys.argv[4])
    output_fasta = sys.argv[5]

    seq = extract_sequence(fasta_path, chromosome, start, end)
    if seq:
        record = SeqRecord(seq, id=f"{chromosome}:{start}-{end}", description="")
        SeqIO.write(record, output_fasta, "fasta")
        print(f"Extracted sequence saved to {output_fasta}")
    else:
        print("Chromosome not found in the FASTA file.")