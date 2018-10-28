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

    """ detect specific SNPS"""    
    detectedSnps  = snp_detector(snps_df)

    snps_df = snps_df[snps_df.geno != "--"].reset_index()
    snps_df = snps_df.drop(columns="index")
    snps_df = snps_df[:num_notes]

    notes = snps_df.geno.map(
        {snp: random.choice(PENTATONIC_SCALE) for snp in snps_df.geno.unique()}
    )
    notes = list(notes)  # we cannot serialize a numpy array

    return [notes, detectedSnps]

def snp_detector(snps_df):
    snps_df = snps_df.set_index("rsid")
    detectedSnps = {}
    detectedSnps['depression'] = depression_detector(snps_df)
    detectedSnps['caffeine'] = caffeine_detector(snps_df)
    detectedSnps['schizophrenia'] = schizophrenia_detector(snps_df)
    return detectedSnps
    
def generic_detector(rsid, positives, snps_df):
    genoDp = snps_df.loc[rsid].geno    
    return any(item for item in map(lambda x: genoDp == x, positives))

def depression_detector(snps_df):    
    depressionSNP = "rs1360780"    
    return generic_detector(depressionSNP, ["CT", "TT"], snps_df)                

def caffeine_detector(snps_df):    
    snp = "rs762551"                    
    return generic_detector(snp, ["AA"], snps_df)

def schizophrenia_detector(snps_df):    
    snp = "rs6277"
    snp2 = "rs1344484"
    return generic_detector(snp, ["CT", "CC"], snps_df) or generic_detector(snp2, ["TT"], snps_df)
