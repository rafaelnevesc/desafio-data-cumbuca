import re

def translate_dna_to_rna_loop(dna: str) -> str:
    regex_dna = r'^[AGCT]*$'
    if not re.match(regex_dna, dna.upper()):
        raise ValueError(f'String deve contar apenas caracteres de DNA')

    repl = {
        "A": "U",
        "T": "A",
        "G": "C",
        "C": "G"
    }
    return ''.join([repl.get(c) for c in dna.upper()])


def translate_dna_to_rna_optimized(dna: str) -> str:
    # Check if the DNA string contains only valid characters
    if not set(dna.upper()).issubset('AGCT'):
        raise ValueError('String must contain only DNA characters')
    
    # Define the DNA to RNA translation dictionary
    dna_to_rna = str.maketrans('AGCT', 'UCGA')

    # Convert the DNA string to uppercase
    dna = dna.upper()

    # Translate the DNA string to RNA
    rna = dna.translate(dna_to_rna)

    return rna


%timeit translate_dna_to_rna_optimized('agctgatgcatcagagctgatgcatcagagctgatgcatcag')
%timeit translate_dna_to_rna_loop('agctgatgcatcagagctgatgcatcagagctgatgcatcag')