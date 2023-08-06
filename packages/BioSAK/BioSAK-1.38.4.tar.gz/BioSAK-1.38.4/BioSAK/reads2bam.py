#!/usr/bin/env python3

import os
import argparse
from BioSAK.global_functions import sep_path_basename_ext


reads2bam_usage = '''
=================================== reads2bam example commands ===================================

module load bowtie/2.3.5.1
module load samtools/1.10
BioSAK reads2bam -p Demo -ref ref.fa -r1 R1.fa -r2 R1.fa -u unpaired.fa -index_ref -t 12
BioSAK reads2bam -p Demo -ref ref.fa -r1 R1.fq -r2 R1.fq -fastq -index_ref -t 12
BioSAK reads2bam -p Demo -ref ref.fa -u unpaired.fa -index_ref -t 12 -tmp -mismatch 2
BioSAK reads2bam -p Demo -ref ref.fa -u unpaired_R1.fa,unpaired_R2.fa -index_ref -t 12 -tmp
BioSAK reads2bam -p Demo -ref ref.fa -u unpaired_R1.fa,unpaired_R2.fa -index_ref -t 12 -tmp -local

==================================================================================================
'''

def cigar_splitter(cigar):

    # get the position of letters
    letter_pos_list = []
    n = 0
    for each_element in cigar:
        if (each_element.isalpha() is True) or (each_element == '='):
            letter_pos_list.append(n)
        n += 1

    # split cigar
    index = 0
    cigar_splitted = []
    while index <= len(letter_pos_list) - 1:
        if index == 0:
            cigar_splitted.append(cigar[:(letter_pos_list[index] + 1)])
        else:
            cigar_splitted.append(cigar[(letter_pos_list[index - 1] + 1):(letter_pos_list[index] + 1)])
        index += 1

    return cigar_splitted


def get_cigar_stats(cigar_splitted):

    # aligned_len: M I X =
    # clipping_len: S
    # mismatch_len: X I D
    # mismatch_pct = mismatch_len / aligned_len
    # aligned_pct  = aligned_len  / (aligned_len + clipping_len)
    # clipping_pct = clipping_len / (aligned_len + clipping_len)

    aligned_len = 0
    clipping_len = 0
    mismatch_len = 0
    for each_part in cigar_splitted:
        each_part_len = int(each_part[:-1])
        each_part_cate = each_part[-1]

        # get aligned_len
        if each_part_cate in {'M', 'm', 'I', 'i', 'X', 'x', '='}:
            aligned_len += each_part_len

        # get clipping_len
        if each_part_cate in ['S', 's']:
            clipping_len += each_part_len

        # get mismatch_len
        if each_part_cate in {'I', 'i', 'X', 'x', 'D', 'd'}:
            mismatch_len += each_part_len

    aligned_pct  = float("{0:.2f}".format(aligned_len * 100 / (aligned_len + clipping_len)))
    clipping_pct = float("{0:.2f}".format(clipping_len * 100 / (aligned_len + clipping_len)))
    mismatch_pct = float("{0:.2f}".format(mismatch_len * 100 / (aligned_len)))

    return aligned_len, aligned_pct, clipping_len, clipping_pct, mismatch_pct


def remove_high_mismatch(sam_in, mismatch_cutoff, sam_out):
    sam_out_handle = open(sam_out, 'w')
    for each_read in open(sam_in):
        each_read_split = each_read.strip().split('\t')
        if each_read.startswith('@'):
            sam_out_handle.write(each_read)
        else:
            cigar = each_read_split[5]
            if cigar == '*':
                sam_out_handle.write(each_read)
            else:
                cigar_splitted = cigar_splitter(cigar)
                r1_aligned_len, r1_aligned_pct, r1_clipping_len, r1_clipping_pct, r1_mismatch_pct = get_cigar_stats(cigar_splitted)
                if r1_mismatch_pct <= mismatch_cutoff:
                    sam_out_handle.write(each_read)
    sam_out_handle.close()


def reads2bam(args):

    output_prefix   = args['p']
    ref_seq         = args['ref']
    index_ref       = args['index_ref']
    r1_seq          = args['r1']
    r2_seq          = args['r2']
    unpaired_seq    = args['u']
    fq_format       = args['fastq']
    local_aln       = args['local']
    max_mismatch    = args['mismatch']
    thread_num      = args['t']
    keep_tmp        = args['tmp']

    ref_path, ref_basename, ref_ext = sep_path_basename_ext(ref_seq)

    cmd_bowtie2_build   = 'bowtie2-build -f %s %s --threads %s' % (ref_seq, ref_basename, thread_num)

    bowtie2_parameter = '--no-unal --xeq'
    if local_aln is True:
        bowtie2_parameter = '--local --no-unal --xeq'

    cmd_bowtie2 = ''
    if (r1_seq is not None) and (r2_seq is not None) and (unpaired_seq is None):
        cmd_bowtie2     = 'bowtie2 -x %s -1 %s -2 %s -S %s_raw.sam -p %s -f %s' % (ref_basename, r1_seq, r2_seq, output_prefix, thread_num, bowtie2_parameter)
        if fq_format is True:
            cmd_bowtie2 = 'bowtie2 -x %s -1 %s -2 %s -S %s_raw.sam -p %s -q %s' % (ref_basename, r1_seq, r2_seq, output_prefix, thread_num, bowtie2_parameter)

    elif (r1_seq is not None) and (r2_seq is not None) and (unpaired_seq is not None):
        cmd_bowtie2     = 'bowtie2 -x %s -1 %s -2 %s -U %s -S %s_raw.sam -p %s -f %s' % (ref_basename, r1_seq, r2_seq, unpaired_seq, output_prefix, thread_num, bowtie2_parameter)
        if fq_format is True:
            cmd_bowtie2 = 'bowtie2 -x %s -1 %s -2 %s -U %s -S %s_raw.sam -p %s -q %s' % (ref_basename, r1_seq, r2_seq, unpaired_seq, output_prefix, thread_num, bowtie2_parameter)

    elif (r1_seq is None) and (r2_seq is None) and (unpaired_seq is not None):
        cmd_bowtie2     = 'bowtie2 -x %s -U %s -S %s_raw.sam -p %s -f %s' % (ref_basename, unpaired_seq, output_prefix, thread_num, bowtie2_parameter)
        if fq_format is True:
            cmd_bowtie2 = 'bowtie2 -x %s -U %s -S %s_raw.sam -p %s -q %s' % (ref_basename, unpaired_seq, output_prefix, thread_num, bowtie2_parameter)
    else:
        print('Please check your input reads files')
        exit()

    cmd_samtools_view   = 'samtools view -bS %s.sam -o %s.bam' % (output_prefix, output_prefix)
    cmd_samtools_sort   = 'samtools sort %s.bam -o %s_sorted.bam' % (output_prefix, output_prefix)
    cmd_samtools_index  = 'samtools index %s_sorted.bam' % output_prefix

    if index_ref is True:
        os.system(cmd_bowtie2_build)
    os.system(cmd_bowtie2)


    if max_mismatch == 100:
        os.system('mv %s_raw.sam %s.sam' % (output_prefix, output_prefix))
    else:
        remove_high_mismatch(('%s_raw.sam' % output_prefix), max_mismatch, ('%s.sam' % output_prefix))
        os.system('rm %s_raw.sam' % output_prefix)


    os.system(cmd_samtools_view)
    os.system(cmd_samtools_sort)
    os.system(cmd_samtools_index)

    if keep_tmp is False:
        os.system('rm %s.sam' % output_prefix)
        os.system('rm %s.bam' % output_prefix)


if __name__ == '__main__':

    reads2bam_parser = argparse.ArgumentParser(usage=reads2bam_usage)

    reads2bam_parser.add_argument('-p',               required=True,                                     help='output prefix')
    reads2bam_parser.add_argument('-ref',             required=True,                                     help='reference sequences')
    reads2bam_parser.add_argument('-index_ref',       required=False, action="store_true",               help='index reference')
    reads2bam_parser.add_argument('-r1',              required=False, default=None,                      help='paired reads r1')
    reads2bam_parser.add_argument('-r2',              required=False, default=None,                      help='paired reads r2')
    reads2bam_parser.add_argument('-u',               required=False, default=None,                      help='unpaired reads')
    reads2bam_parser.add_argument('-fastq',           required=False, action="store_true",               help='reads in fastq format')
    reads2bam_parser.add_argument('-local',           required=False, action="store_true",               help='perform local alignment')
    reads2bam_parser.add_argument('-mismatch',        required=False, type=int, default=100,             help='maximum mismatch pct allowed, between 1-100, default: 100')
    reads2bam_parser.add_argument('-t',               required=False, type=int, default=1,               help='number of threads, default: 1')
    reads2bam_parser.add_argument('-tmp',             required=False, action="store_true",               help='keep temporary files')

    args = vars(reads2bam_parser.parse_args())

    reads2bam(args)
