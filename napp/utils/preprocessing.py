import numpy as np
import pandas as pd
from tqdm import tqdm


def get_len_chr(hic, name_chr):
    """
    :param hic: hic object
    :param name_chr: name of chromosome
    :return: length of chromosome with name name_chr
    """
    for chrom in hic.getChromosomes():
        if chrom.name == name_chr:
            return chrom.length
    raise RuntimeError("Not found chromosome with name " + name_chr)


def getHicMatrixOneChr(hic,
                       name_chr,
                       resolution,
                       chunk_size=2000000,
                       output_file=None):
    """
    :param hic: hic object
    :param name_chr: name of chromosome
    :param resolution: size of bin
    :param chunk_size: inner parameter -- using for contructing result matrix with non-high-permormance CPU
    :param output_file: file for saving or loading
    :return: hi-c matrix
    """

    if output_file is not None:
        return np.load(output_file)

    matrix_object_chr = hic.getMatrixZoomData(name_chr, name_chr, "observed",
                                              "KR", "BP", resolution)
    len_chr = get_len_chr(hic, name_chr)

    all_numpy_matrix_chr = None
    for i in tqdm(range(0, len_chr, chunk_size), "Constructing hic-matrix"):
        tmp_list_numpy_matrix_chr = []
        for j in range(0, len_chr, chunk_size):
            chunk_numpy_matrix_chr = matrix_object_chr.getRecordsAsMatrix(
                i,
                min(i + chunk_size, len_chr) - 1, j,
                min(j + chunk_size, len_chr) - 1)
            # appending by columns
            tmp_list_numpy_matrix_chr.append(chunk_numpy_matrix_chr)
        # concat by rows
        concat_list_numpy_matrix_chr = np.concatenate(
            tmp_list_numpy_matrix_chr, axis=1)
        if all_numpy_matrix_chr is None:
            all_numpy_matrix_chr = concat_list_numpy_matrix_chr
        else:
            all_numpy_matrix_chr = np.concatenate(
                (all_numpy_matrix_chr, concat_list_numpy_matrix_chr), axis=0)

    output_file = '_'.join(["hic_matrix", name_chr, str(resolution)]) + ".npy"
    np.save(f'caching_data/inner/{output_file}', all_numpy_matrix_chr)
    return all_numpy_matrix_chr


def get_ncount_matrix(ncount_file, is_last_column_problem=False):
    """
    :param ncount_file: file with ncounts
    :param is_last_column_problem: inner parameter -- if ncount_file consists problem with last column
    :return: dataframe with ncounts
    """
    ncounts_df = pd.read_csv(ncount_file, header=None, sep='\t')
    ncounts_df.drop([0, 1, 2, 3], axis=1, inplace=True)
    ncounts_array = ncounts_df.to_numpy()
    if is_last_column_problem:
        ncounts_array = np.concatenate(
            (ncounts_array, np.array([ncounts_array.T[-1]]).T), axis=1)
    return ncounts_array


def get_density_per_bin(name_bed_file, resolution, name_chr, num_bins,
                        name_to_type):
    """
    :param name_bed_file: bed file with annotation of anything (repeat, CDS...)
    :param resolution: size of the bins
    :param name_chr: name of chromosome
    :param num_bins: number of bins
    :param name_to_type: dict -- (name -> type of repeat)
    :return: density per each bin with given resolution
    """
    overlap_parts = np.zeros((len(name_to_type), num_bins))
    with open(name_bed_file) as f:
        for line in f:
            row = line.strip().split()
            if row[0] != name_chr or row[3] not in name_to_type:
                continue
            l, r = int(row[1]), int(row[2])
            ind = name_to_type[row[3]]
            l_i = l // resolution
            r_i = r // resolution
            for i in range(l_i, r_i):
                cur_r = (i + 1) * resolution
                overlap_parts[ind, i] += (cur_r - l)
                l = cur_r
            else:
                overlap_parts[ind, r_i] += (r - l + 1)

    return overlap_parts


def get_gc_content_per_bin(genome, resolution):
    """
    :param genome:
    :param resolution: size of the bins
    :return: GC content per bin
    """
    len_genome = len(genome)
    num_bins = len_genome // resolution + (len_genome % resolution != 0)
    gc_content_per_bin = np.zeros(num_bins)
    cur_gc = 0
    for (i, nucl) in enumerate(tqdm(genome, "Getting GC-content")):
        if (i % resolution == 0) and i > 0:
            gc_content_per_bin[(i // resolution) - 1] = cur_gc
            cur_gc = 0
        cur_gc += (nucl == 'G' or nucl == 'C')
    gc_content_per_bin[-1] = cur_gc

    return gc_content_per_bin


def get_distance_between_pair(resolution, len_genome):
    num_bins = len_genome // resolution + (len_genome % resolution != 0)
    distance_between_pair = np.zeros((num_bins, num_bins))
    for i in range(num_bins - 1):
        for j in range(num_bins - 1):
            distance_between_pair[i, j] = abs(j - i) * resolution
        distance_between_pair[-1, i] = len_genome - resolution * (i + 1)
        distance_between_pair[i, -1] = len_genome - resolution * (i + 1)
    return distance_between_pair


name_to_gene_type = {'CDS': 0, 'gene': 1, 'intron': 2}
