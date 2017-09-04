import os
import sys
import datetime
import csv
import argparse

def main():
    parser = argparse.ArgumentParser(description="List the path type (file, directory, link, mount, etc.) creation time (ctime), access time (atime), and modification time (mtime) in seconds, utc time and local time, recursively for all files at the given path.")
    parser.add_argument('paths', metavar='path', type=str, nargs='+',
            help='The paths to search')
    args = parser.parse_args()

    writer = csv.DictWriter(sys.stdout, ['path','type','size','ctime', 'ctime_utc', 'ctime_local', 'atime', 'atime_utc', 'atime_local', 'mtime', 'mtime_utc', 'mtime_local'])
    writer.writeheader()

    for path in args.paths:
        if os.path.isfile(path):
            write_details(writer, path)
        else:
            for root, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    write_details(writer, os.path.join(root, filename))


def write_details(writer, path):
    results = get_details(path)
    if results is not None:
        writer.writerow(results)


def get_details(path):
    out = {}

    try:
        ctime = os.path.getctime(path)
        atime = os.path.getatime(path)
        mtime = os.path.getmtime(path)

        type = '?'
        if os.path.isfile(path):
            type = 'file'
        elif os.path.isdir(path):
            type = 'dir'
        elif os.path.islink(path):
            type = 'link'
        elif os.path.ismount(path):
            type = 'mount'

        out['path'] = path
        out['type'] = type
        out['size'] = os.path.getsize(path)

        out['ctime'] = ctime
        out['ctime_utc'] = datetime.datetime.utcfromtimestamp(ctime).isoformat()
        out['ctime_local'] = datetime.datetime.fromtimestamp(ctime).isoformat()

        out['atime'] = atime
        out['atime_utc'] = datetime.datetime.utcfromtimestamp(atime).isoformat()
        out['atime_local'] = datetime.datetime.fromtimestamp(atime).isoformat()

        out['mtime'] = mtime
        out['mtime_utc'] = datetime.datetime.utcfromtimestamp(mtime).isoformat()
        out['mtime_local'] = datetime.datetime.fromtimestamp(mtime).isoformat()

    except OSError as e:
        print(e)
        out = None
    return out


if __name__ == "__main__":
	main()
