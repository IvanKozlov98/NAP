import argparse

from src.utils.preprocessing import *
from src.utils.utils import *


def preprocessing_common_data(name_chr, resolution, genome_file,
                              bed_file_with_repeat_annotation,
                              bed_file_with_gene_annotation, ncounts_file):
    """

    :param name_chr:
    :param resolution:
    :param genome_file:
    :param bed_file_with_repeat_annotation:
    :param bed_file_with_gene_annotation:
    :param ncounts_file:
    :return:
    """
    ncounts_matrix = get_ncount_matrix(ncounts_file,
                                       is_last_column_problem=True)
    num_bins = ncounts_matrix.shape[0]
    gene_type_density_per_bin = get_density_per_bin(
        name_bed_file=bed_file_with_gene_annotation,
        resolution=resolution,
        name_chr=name_chr,
        num_bins=num_bins,
        name_to_type=name_to_gene_type)
    repeat_density_per_bin = get_density_per_bin(
        name_bed_file=bed_file_with_repeat_annotation,
        resolution=resolution,
        name_chr=name_chr,
        num_bins=num_bins,
        name_to_type=get_name_to_type_repeat())
    genome = get_genome_seq(genome_file)
    gc_content_per_bin = get_gc_content_per_bin(genome, resolution)
    distance_between_pair = get_distance_between_pair(resolution, len(genome))

    data_per_bin = pd.DataFrame.from_dict({
        "retroelement":
        repeat_density_per_bin[0],
        "dna_transposon":
        repeat_density_per_bin[1],
        "simple_repeat":
        repeat_density_per_bin[2],
        "unclassified":
        repeat_density_per_bin[3],
        "other":
        repeat_density_per_bin[4],
        "gc_content":
        gc_content_per_bin,
        "CDS":
        gene_type_density_per_bin[0],
        "gene":
        gene_type_density_per_bin[1],
        "intron":
        gene_type_density_per_bin[2]
    })

    data_per_pair_bin = cartesian(data_per_bin, data_per_bin)
    # add information about gomology
    data_per_pair_bin['gomology'] = ncounts_matrix.flatten()
    # add information about distance
    data_per_pair_bin['distance'] = distance_between_pair.flatten()

    return data_per_pair_bin


def parse_cmdline():
    parser = argparse.ArgumentParser(description="Make dataset based on DNA.")
    parser.add_argument("-c",
                        "--name_chr",
                        type=str,
                        help="name of chomosome",
                        required=True)
    parser.add_argument("-r",
                        "--resolution",
                        type=str,
                        help="resolution",
                        required=True)
    parser.add_argument("-chr",
                        "--chromosome",
                        type=str,
                        help="chromosome file",
                        required=True)
    parser.add_argument("-rp",
                        "--repeat",
                        type=str,
                        help="repeat annotation file",
                        required=True)
    parser.add_argument("-g",
                        "--gene",
                        type=str,
                        help="gene annotation file",
                        required=True)
    parser.add_argument("-gm",
                        "--gomology",
                        type=str,
                        help="gomology file",
                        required=True)
    parser.add_argument("-o",
                        "--output",
                        type=str,
                        help="name of output file with common data",
                        required=True)

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_cmdline()
    common_data = preprocessing_common_data(
        name_chr=args.name_chr,
        resolution=int(args.resolution),
        genome_file=args.chromosome,
        bed_file_with_repeat_annotation=args.repeat,
        bed_file_with_gene_annotation=args.gene,
        ncounts_file=args.gomology)
    print('Common data was computed')
    print('Start saving this')
    common_data_path = get_path_to_common_data(args.output)
    common_data.to_csv(common_data_path, index=False)
    print('Finish saving')
    print(f'Common data was computed and saved into {common_data_path}')
