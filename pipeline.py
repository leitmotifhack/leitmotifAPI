from io import StringIO
import pandas as pd
import random


PENTATONIC_SCALE = [440, 495, 556.875, 660, 742.5]  # A, B, C#, E, F
FREQ2MIDI = {
    440: 69,  # A
    495: 71,  # B
    556.875: 73,  # C sharp
    660: 76,  # E
    742.5: 78,  # F
}


def length_gen(n):
    """generate a semi-random note length"""
    return int(3.5 + math.sin(n / 2) + (2.5 * math.cos(n)) + random.random())


def transform_23_and_me_dataset_to_notes(_23_and_me_txt, num_notes=1000):
    """transform 23&me snps randomly into notes"""
    snps_df = pd.read_csv(
        StringIO(_23_and_me_txt),
        header=20,
        names=["rsid", "chrom", "pos", "geno"],
        delimiter="\t",
        low_memory=False,
    )
    snps_df = snps_df[snps_df.geno != "--"].reset_index()
    snps_df = snps_df.drop(columns="index")
    snps_df = snps_df[:num_notes]
    notes = snps_df.geno.map(
        {snp: random.choice(PENTATONIC_SCALE) for snp in snps_df.geno.unique()}
    )
    notes = list(notes)  # we cannot serialize a numpy array
    return notes
