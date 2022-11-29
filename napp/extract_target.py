"""Target module"""

import argparse

import hicstraw
import numpy as np

from napp.utils.ml import assign_class
from napp.utils.preprocessing import get_hic_matrix_one_chr
from napp.utils.utils import get_path_to_targets


def get_target(hic_file, name_chr, resolution, type_target):
    """
    :param hic_file: file or url with hic-data
    :param name_chr: name of chromosome
    :param resolution: size of the bin
    :param type_target: maybe one of "Regression", "Binary", "Multiclass"
    :return: target based on hic-data
    """
    hic = hicstraw.HiCFile(hic_file)
    hic_matrix = get_hic_matrix_one_chr(hic, name_chr, resolution)
    regression_target = hic_matrix.flatten()
    if type_target == "Regression":
        return regression_target
    elif type_target == "Binary":
        threshold = 10
        return (regression_target > threshold) * 1
    elif type_target == "Multiclass":
        return np.array(list(map(assign_class, regression_target)))
    else:
        raise RuntimeError("Type target must be one of "
                           "{\"Regression\", \"Binary\", \"Multiclass\"}")


def parse_cmdline():
    """Parse cmdline arguments"""
    parser = argparse.ArgumentParser(
        description="Extract target for model from hic-data")
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
    parser.add_argument("-hic", type=str, help="hic file", required=True)
    parser.add_argument("-m",
                        "--ml_task",
                        type=str,
                        help="type of task",
                        required=True,
                        choices=["Regression", "Binary", "Multiclass"])
    parser.add_argument("-o",
                        "--output",
                        type=str,
                        help="name of output file with target",
                        required=True)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    """Main function"""
    args = parse_cmdline()
    target = get_target(hic_file=args.hic,
                        name_chr=args.name_chr,
                        resolution=int(args.resolution),
                        type_target=args.ml_task)
    target_path = get_path_to_targets(args.output)
    np.save(target_path, target)
    print(f"Target was computed and saved into {target_path}")
