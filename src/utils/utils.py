from tqdm import tqdm
import numpy as np
from scipy.stats import norm
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
from Bio import SeqIO


def divide_by_distance(matrix, resolution, upto=1000000):
    """
    Extract grouped pairs of regions based on their genomic distance
    :param matrix: considering matrix
    :param resolution: size of bin
    :param upto: size of window
    :return: two dim numpy array - a[i] -> [count between i1 bin and i2 bin with distance i * resolution]
    """
    n, m = matrix.shape
    assert n == m
    up = min(upto // resolution, m)
    group_by_distance = [[] for _ in range(up)]
    for i in tqdm(range(0, n), "Dividing by distance"):
        for j in range(0, n):
            dist = abs(i - j)
            if dist >= up:
                continue
            group_by_distance[dist].append(matrix[i, j])
    return group_by_distance


def get_auc_distance_stratified_correlation(matrix_1, matrix_2, resolution):
    """
    :param matrix_1:
    :param matrix_2:
    :param resolution: size of bin
    :return: summarized the distance-stratified Pearson’s correlation curve into the area under the curve
    """
    group_by_distance_1 = divide_by_distance(matrix_1, resolution)
    group_by_distance_2 = divide_by_distance(matrix_2, resolution)
    n = len(group_by_distance_1)
    f = [np.corrcoef(group_by_distance_1[i], group_by_distance_2[i])[0, 1] for i in range(n)]
    auc = 0
    for i in range(n - 1):
        auc += (f[i] + f[i + 1])
    return auc / (2 * (n - 1))


def get_random_matrix(size, mean, std):
    """
    :return: random matrix
    """
    return np.abs(norm.rvs(loc=mean, scale=std, size=(size, size)))


def get_random_diag_matrix(size, max_val, std):
    """
    :return: random matrix in which diagonal elements more than other
    """
    random_diag_matrix = np.abs(norm.rvs(loc=max_val, scale=std, size=(size, size)))
    for i in tqdm(range(size), "Generation of random diag matrix"):
        for j in range(size):
            random_diag_matrix[i, j] = abs(random_diag_matrix[i, j] - abs(i - j))

    return random_diag_matrix


def plot_hic_matrix(hic_matrix):
    REDMAP = LinearSegmentedColormap.from_list("bright_red", [(1, 1, 1), (1, 0, 0)])

    # helper function for plotting
    def plot_hic_map(dense_matrix, maxcolor):
        plt.matshow(dense_matrix, cmap=REDMAP, vmin=0, vmax=maxcolor)
        plt.show()

    plot_hic_map(hic_matrix, 30)


def get_name_to_type_repeat():
    retroelements = {'SINE?', 'LTR/Pao', 'LTR/Unknown', 'LTR', 'LTR/Gypsy', 'LTR/Copia', 'LTR/ERVK', 'LINE/I',
                     'LINE/L2', 'LINE/CR1', 'LINE/R1', 'LINE/L1-Tx1', 'LINE/RTE', 'LINE/RTE-BovB', 'LINE/I-Jockey'}
    dna_transposons = {'DNA/PIF-Harbinger', 'DNA/Merlin', 'DNA/hAT-Ac', 'DNA/hAT-hAT5', 'DNA/hAT-Tip100', 'DNA/P',
                       'DNA/TcMar-Mariner', 'DNA/CMC-EnSpm', 'DNA/CMC-Mirage', 'DNA/Maverick', 'DNA/Zisupton',
                       'DNA/TcMar-Tc1', 'DNA/TcMar-ISRm11', 'DNA/hAT-Charlie', 'DNA/Dada', 'DNA/PiggyBac', }
    simple_repeats = {'Simple_repeat'}
    unclassified = {'Unknown'}
    other = {'rRNA', 'tRNA', 'Satellite', 'Low_complexity', 'RC/Helitron', 'snRNA'}
    name_to_type_repeat = dict()
    for retroelement in retroelements:
        name_to_type_repeat[retroelement] = 0  # "retroelement"
    for dna_transposon in dna_transposons:
        name_to_type_repeat[dna_transposon] = 1  # "dna_transposon"
    for simple_repeat in simple_repeats:
        name_to_type_repeat[simple_repeat] = 2  # "simple_repeat"
    for u in unclassified:
        name_to_type_repeat[u] = 3  # "unclassified"
    for o in other:
        name_to_type_repeat[o] = 4  # "other"

    return name_to_type_repeat


def get_genome_seq(path):
    """
    :param path: path to fasta file which consist only one contig
    :return: string of genome
    """
    return next(SeqIO.parse(path, "fasta")).seq


def cartesian(df1, df2):
    return ( df1.assign(key=1)
            .merge(df2.assign(key=1), on="key")
            .drop("key", axis=1))


def cartesian_numpy(x, y):
    return np.transpose([np.repeat(x, len(y)), np.tile(y, len(x))])


def simple_paint(ys, title, x_name, y_name):
    plt.title(title)
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    xs = np.arange(ys.size)
    plt.plot(xs, ys)
    plt.show()


def get_path_to_models(model_name):
    return f'caching_data/models/{model_name}'


def get_path_to_common_data(common_data):
    return f'caching_data/common_data/{common_data}'


def get_path_to_predictions(predictions):
    return f'caching_data/predictions/{predictions}'


def get_path_to_targets(targets):
    return f'caching_data/targets/{targets}'
