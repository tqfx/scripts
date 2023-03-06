#!/usr/bin/env bash

usage()
{
    echo "USAGE: $0 [OPTIONS]"
    echo "OPTIONS:"
    echo "  -v, --version [NUM]    clang version"
    exit
}

if [ $# == 0 ]; then
    usage
fi

while [ $# -gt 0 ]; do
    case "$1" in
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

if [ "$version" -gt 0 ] 2>/dev/null; then
    for i in $(ls -B /usr/bin/*-$version); do
        name=$(basename ${i/-$version/})
        sudo ln -vsb /usr/lib/llvm-$version/bin/$name /usr/bin/$name
    done
fi
