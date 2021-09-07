import sys
from multiprocessing import Queue

from searcher import Searcher
from zipper import Zipper

if __name__ == '__main__':
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    workers = int(sys.argv[3])

    files_info = Queue()

    searcher = Searcher(input_dir, files_info, workers)
    zipper = Zipper(output_dir, files_info, workers)

    searcher.start()
    zipper.start()

    searcher.join()
    zipper.join()
