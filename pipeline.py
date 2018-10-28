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


def transform_23_and_me_dataset_to_notes(_23_and_me_fp, num_notes=1000):
    """transform 23&me snps randomly into notes"""
    snps_df = pd.read_csv(
        _23_and_me_fp,
        header=20,
        names=["rsid", "chrom", "pos", "geno"],
        delimiter="\t",
        low_memory=False,
    )
    snps_df = snps_df[snps_df.geno != "--"]
    snps_df = snps_df.set_index('rsid')

    # search the SNPS
    caffeine = caffeine_detector(snps_df)
    schizophrenia = schizophrenia_detector(snps_df)
    depression = depression_detector(snps_df)

    # map to notes
    snps_df = snps_df.sample(n=1000)  # crop
    notes = snps_df.geno.map(
        {snp: random.choice(PENTATONIC_SCALE) for snp in snps_df.geno.unique()}
    )
    notes = list(notes)  # we cannot serialize a numpy array

    return notes, depression, caffeine, schizophrenia


def generic_detector(rsid, positive_snps, snps_df):
    try:
        snp = snps_df.loc[rsid].geno
    except KeyError:
        raise IOError(snps_df.head())
    return any(snp == positive_snp for positive_snp in positive_snps)


def depression_detector(snps_df):
    depression_snp = "rs1360780"
    return generic_detector(depression_snp, ["CT", "TT"], snps_df)


def caffeine_detector(snps_df):
    caffeine_snp = "rs762551"
    return generic_detector(caffeine_snp, ["AA"], snps_df)


def schizophrenia_detector(snps_df):
    return generic_detector("rs6277", ["CT", "CC"], snps_df) or generic_detector(
        "rs1344484", ["TT"], snps_df
    )
