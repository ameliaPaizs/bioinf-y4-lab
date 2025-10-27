"""
Exercițiu 04 — FASTQ QC pe date proprii

TODO:
- Citiți fișierul vostru FASTQ din data/work/<handle>/lab03/:
    your_reads.fastq  sau  your_reads.fastq.gz
- Calculați statistici:
    * număr total de citiri
    * lungimea medie a citirilor
    * proporția bazelor 'N'
    * scorul Phred mediu
- Salvați raportul în:
    labs/03_formats&NGS/submissions/<handle>/qc_report_<handle>.txt
"""

import os
import gzip
from pathlib import Path
from Bio import SeqIO

# TODO: înlocuiți <handle> cu username-ul vostru GitHub
handle = "ameliaPaizs"

in_fastq_plain = Path(f"data/work/{handle}/lab03/SRR390728_1.fastq")
in_fastq_gz = Path(f"data/work/{handle}/lab03/SRR390728_1.fastq.gz")
out_report = Path(f"labs/03_formats&NGS/submissions/{handle}/qc_report_{handle}.txt")
out_report.parent.mkdir(parents=True, exist_ok=True)

# Selectați fișierul existent
if in_fastq_plain.exists():
    reader = SeqIO.parse(str(in_fastq_plain), "fastq")
elif in_fastq_gz.exists():
    reader = SeqIO.parse(gzip.open(in_fastq_gz, "rt"), "fastq")
else:
    raise FileNotFoundError(
        f"Nu am găsit nici {in_fastq_plain} nici {in_fastq_gz}. "
        f"Rulați întâi ex03_fetch_fastq.py sau copiați un FASTQ propriu."
    )

num_reads = 0
total_length = 0
total_n = 0
total_phred = 0
total_bases = 0

# QC
for record in reader:
    seq_str = str(record.seq)
    phred = record.letter_annotations["phred_quality"]

    num_reads += 1
    total_length += len(seq_str)
    total_n += seq_str.upper().count("N")
    total_phred += sum(phred)
    total_bases += len(phred)

# Calcul statistici
if num_reads > 0:
    len_mean = total_length / num_reads
else:
    len_mean = 0.0

if total_bases > 0:
    n_rate = total_n / total_bases
    phred_mean = total_phred / total_bases
else:
    n_rate = 0.0
    phred_mean = 0.0

# Scriere raport
with open(out_report, "w", encoding="utf-8") as out:
    out.write(f"Reads: {num_reads}\n")
    out.write(f"Mean length: {len_mean:.2f}\n")
    out.write(f"N rate: {n_rate:.4f}\n")
    out.write(f"Mean Phred: {phred_mean:.2f}\n")

print(f"[OK] QC report -> {out_report.resolve()}")
