#!/usr/bin/env bash

usage()
{
    echo "USAGE: $0 [OPTIONS]"
    echo "OPTIONS:"
    echo "  -v, --version [NUM]    clang version"
    echo "  -h, --help             display this help and exit"
    exit 0
}

while [ $# -gt 0 ]; do
    case "$1" in
        -h|--help)
            shift
            usage
            ;;
        -v|--version)
            shift
            version="$1"
            ;;
        *)
            version="$1"
            ;;
    esac
    shift
done

if [ -z $version ]; then
    version=0
    for ver in $(echo /usr/lib/llvm-*); do
        ver=${ver/\/usr\/lib\/llvm-/}
        if [ $ver -gt $version ]; then
            version=$ver
        fi
    done
fi

if [ -d /usr/lib/llvm-$version ]; then
    for i in $(ls -B /usr/bin/*-$version); do
        name=$(basename ${i/-$version/})
        sudo ln -vsf /usr/lib/llvm-$version/bin/$name /usr/bin/$name
    done
fi
