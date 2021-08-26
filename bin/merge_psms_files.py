import pandas as pd
import sys
import os
import argparse
from tqdm import tqdm


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('input_psm_filename')
parser.add_argument('input_files_filename')
parser.add_argument('output_merged_filename')

args = parser.parse_args()

files_df = pd.read_csv(args.input_files_filename, sep='\t', header=None, index_col=False, names=["index", "filename"])

index_to_filename = {}
for object in files_df.to_dict("records"):
    index_to_filename[object["index"]] = object["filename"]

with open(args.output_merged_filename, 'w') as out_file:
    out_file.write("scan\tpeptide\tcharge\tfilename\n")
    for line in tqdm(open(args.input_psm_filename)):
        splits = line.rstrip().split("\t")
        out_file.write("{}\t{}\t{}\t{}\n".format(splits[0], splits[1], splits[2], index_to_filename[int(splits[3])]))