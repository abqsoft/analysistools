"""
Identifies files at the given path where all timestamps (modify, create, access) are different

Requires Python2.7 or later
"""
import os
import argparse
import csv
import sys


def main():
    parser = argparse.ArgumentParser(description="List all files where creation time (ctime), access time (atime), and modification time (mtime) are all different")
    parser.add_argument('paths', metavar='path', type=str, nargs='+',
            help='The paths to search')
    args = parser.parse_args()

    writer = csv.DictWriter(sys.stdout, ['path','ctime','atime','mtime'])
    writer.writeheader()

    for path in args.paths:
        if os.path.isfile(path):
            write_timestamps(writer, path)
        else:
            # Note: Python 2 doesn't support glob.iglob, so use os.walk instead to support both Py2 & Py3
            for root, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    write_timestamps(writer, os.path.join(root, filename))


def write_timestamps(writer, path):
    ts = get_timestamps(path)
    if ts is not None:
        writer.writerow(ts)


def get_timestamps(path):
    out = {}
    try:
        out['path'] = path
        out['ctime'] = os.path.getctime(path)
        out['atime'] = os.path.getatime(path)
        out['mtime'] = os.path.getmtime(path)
    except OSError as e:
        print(e)
        out = None
    return out


if __name__ == "__main__":
    main()
