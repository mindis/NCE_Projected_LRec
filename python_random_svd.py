import argparse
from scipy.sparse import *
import numpy as np
import mxnet as mx
from sklearn.utils.extmath import randomized_svd

# Note: This file is for Java command call only, not part of this package at all.

def check_int_positive(value):
    ivalue = int(value)
    if ivalue < 0:
         raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue


def check_float_positive(value):
    ivalue = float(value)
    if ivalue <= 0:
         raise argparse.ArgumentTypeError("%s is an invalid positive float value" % value)
    return ivalue

def shape(s):
    try:
        num = int(s)
        return num
    except:
        raise argparse.ArgumentTypeError("Sparse matrix shape must be integer")


def load_csv(path, name, shape=(1010000, 2262292)):
    data = np.genfromtxt(path + name, delimiter=',')
    matrix = csr_matrix((data[:, 2], (data[:, 0].astype('int32'), data[:, 1].astype('int32'))), shape=shape)
    # create npz for later convenience
    save_npz(path + "rating.npz", matrix)
    return matrix


def save_mxnet(matrix, path, name):
    if not isinstance(matrix, np.ndarray):
        matrix = matrix.todense()
    mx_array = mx.nd.array(matrix)
    mx.nd.save(path + name, mx_array)


def main(args):
    print("Reading CSV")
    matrix_input = load_csv(path=args.path, name=args.train, shape=args.shape)
    print("Perform SVD")

    boosted_matrix = matrix_input*(1 + args.boost*matrix_input)

    P, sigma, Qt = randomized_svd(boosted_matrix,
                                  n_components=args.rank,
                                  n_iter=args.iter,
                                  random_state=None)

    RQ = matrix_input.dot(csc_matrix(Qt).T)
    print("Save U,S,V")
    save_mxnet(P, args.path, args.user)
    save_mxnet(Qt.T, args.path, args.item)
    save_mxnet(sigma, args.path, args.sigm)
    save_mxnet(RQ, args.path, args.rv)
    print("Python Job Done")


if __name__ == "__main__":
    # Commandline arguments
    parser = argparse.ArgumentParser(description="LRec")
    parser.add_argument('-i', dest='iter', type=check_int_positive, default=4)
    parser.add_argument('-r', dest='rank', type=check_int_positive, default=100)
    parser.add_argument('-d', dest='path', default="/media/wuga/Storage/python_project/wlrec/IMPLEMENTATION_Projected_LRec/data/")
    parser.add_argument('-f', dest='train', default='RTrain.csv')
    parser.add_argument('-u', dest='user', default='U.nd')
    parser.add_argument('-v', dest='item', default='V.nd')
    parser.add_argument('-s', dest='sigm', default='S.nd')
    parser.add_argument('-rv', dest='rv', default='RV.nd')
    parser.add_argument('--boost', dest='boost', type=check_float_positive, default=1)
    parser.add_argument('--shape', help="CSR Shape", dest="shape", type=shape, nargs=2)
    args = parser.parse_args()

    main(args)