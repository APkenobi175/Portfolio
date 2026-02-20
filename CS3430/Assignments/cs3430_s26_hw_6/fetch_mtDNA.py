# fetch_mtDNA.py
# ---------------------------------------------------------------------------------------
#
# CS3430 S26: Scientific Computing
# HW 6, Problem 2: Randomness of Biological Sequences
#
# Copyright (C) Vladimir Kulyukin. All rights reserved.
# For personal study by my students enrolled in CS3430 S26: Scientific Computing, SoC, CoE, USU.
# No redistribution or online posting (e.g., Course Hero, Chegg, GitHub, ChatGPT, Gemini,
# Co-Pilot, Claude, DeepSeek, public drives, any LLMs) without prior written permission.
#
# I used this script to generate mtDNA_sequence.txt for Problem 2.
# ---------------------------------------------------------------------------------------

import requests
from typing import Final

NCBI_URL: Final[str] = "https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi"
ACCESSION: Final[str] = "NC_012920.1"

def fetch_mtDNA_sequence() -> str:
    """
    Fetch the human mitochondrial reference genome (NC_012920.1)
    from NCBI in FASTA format and return the raw DNA sequence
    (without FASTA header or line breaks).

    Returns
    -------
    str
        A single uppercase DNA string of length 16569.
    """
    params = {
        "id": ACCESSION,
        "db": "nuccore",
        "report": "fasta",
        "retmode": "text",
    }

    response = requests.get(NCBI_URL, params=params, timeout=10)
    response.raise_for_status()

    fasta_text = response.text.splitlines()

    # Remove FASTA header (first line begins with '>')
    sequence_lines = [line.strip() for line in fasta_text if not line.startswith(">")]

    sequence = "".join(sequence_lines).upper()

    return sequence


if __name__ == "__main__":
    seq = fetch_mtDNA_sequence()
    print(f"Sequence length: {len(seq)}")
    #print(seq[:100])  # preview first 100 bases
    print(seq)
