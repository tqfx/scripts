#!/usr/bin/env python
import argparse
import hashlib
import os


def hash_(file: str, name: str = "MD5", BUFSIZ=0x2000) -> str:
    hashes = hashlib.new(name)
    with open(file, "rb") as f:
        buffer = f.read(BUFSIZ)
        while buffer:
            hashes.update(buffer)
            buffer = f.read(BUFSIZ)
    return hashes.hexdigest()


class rm:
    def __init__(self, remove=False, rename=False, verbose=False) -> None:
        self.verbose = verbose
        self.rename_ = rename
        self.remove_ = remove

    def __call__(self, top):
        for dirpath, dirnames, filenames in os.walk(top):
            del dirnames
            if self.verbose:
                print(dirpath)
            self.files = []
            for filename in filenames:
                filename = os.path.join(dirpath, filename)
                filesize = os.path.getsize(filename)
                filehash = hash_(filename)
                self.files.append((filename, filesize, filehash))
            if self.files:
                self.files.sort(key=lambda x: x[1])
                self.init().rename().remove().exit()
            del self.files
        return self

    def exec(self, filenames):
        self.files = []
        for filename in filenames:
            if not os.path.isfile(filename):
                continue
            filesize = os.path.getsize(filename)
            filehash = hash_(filename)
            self.files.append((filename, filesize, filehash))
        if self.files:
            self.files.sort(key=lambda x: x[1])
            self.init().rename().remove().exit()
        del self.files

    def init(self):
        n = len(self.files)
        self.stats = [0] * n
        for i, file in enumerate(self.files):
            if not file[1]:
                self.stats[i] = -1
                continue
            for j in range(i + 1, n):
                if self.files[i][1] != self.files[j][1]:
                    break
                if self.files[i][2] == self.files[j][2]:
                    ti = os.path.getmtime(self.files[i][0])
                    tj = os.path.getmtime(self.files[j][0])
                    if ti > tj:
                        self.stats[i] = 1
                    else:
                        self.stats[j] = 1
        return self

    def rename(self):
        namefmt = "%0{}x".format(len("%x" % self.files[-1][1]))
        for i, file in enumerate(self.files):
            if self.stats[i] == 0:
                dirname, srcname = os.path.split(file[0])
                srcname, suffix = os.path.splitext(srcname)
                dstname = namefmt % (file[1]) + file[2][:8]
                filename = os.path.join(dirname, dstname + suffix)
                if file[0] != filename:
                    if self.rename_:
                        os.rename(file[0], filename)
        return self

    def remove(self):
        for i, file in enumerate(self.files):
            if self.stats[i] != 0:
                if self.remove_:
                    os.remove(file[0])
                if self.verbose:
                    print("删除", file[0], file[1])
        return self

    def exit(self):
        del self.stats


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dirs", nargs='+', help="dirs")
    parser.add_argument("-r", "--remove", dest="remove", action="store_true")
    parser.add_argument("-m", "--rename", dest="rename", action="store_true")
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        help="explain what is being done",
    )
    args = parser.parse_args()
    main = rm(remove=args.remove, rename=args.rename, verbose=args.verbose)
    for dir in args.dirs:
        if os.path.isdir(dir):
            main(dir)
    main.exec(args.dirs)
