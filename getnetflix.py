from utils.io import save_numpy, load_netflix
from utils.argument import shape, ratio
from providers.split import time_ordered_split
import argparse
from utils.progress import WorkSplitter


def main(args):
    progress = WorkSplitter()

    progress.section("Load Raw Data")
    rating_matrix, timestamp_matrix = load_netflix(path=args.folder, shape=args.shape)
    progress.section("Split CSR Matrices")
    rtrain, rvalid, rtest = time_ordered_split(rating_matrix=rating_matrix, timestamp_matrix=timestamp_matrix,
                                               ratio=args.ratio, implicit=args.implicit)
    progress.section("Save NPZ")
    save_numpy(rtrain, args.path, "Rtrain")
    save_numpy(rvalid, args.path, "Rvalid")
    save_numpy(rtest, args.path, "Rtest")

if __name__ == "__main__":
    # Commandline arguments
    parser = argparse.ArgumentParser(description="Data Preprocess")
    parser.add_argument('--implicit', dest='implicit', action='store_true')
    parser.add_argument('-r', dest='ratio', type=ratio, default='0.5,0.2,0.3')
    parser.add_argument('-f', dest='folder',
                        default="/media/wuga/Storage/data/netflix/download/training_set")
    parser.add_argument('-d', dest='path', default='/media/wuga/Storage/data/netflix/')
    parser.add_argument('--shape', help="CSR Shape", dest="shape", type=shape, nargs=2)
    args = parser.parse_args()

    main(args)