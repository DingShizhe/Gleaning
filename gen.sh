#!/usr/bin/env bash

src_dir=$1
des_dir=$2

function gen_dir {
    for file in `ls $src_dir$1`; do
        echo 'Converting File:' $1'/'$file
        ./gen.py $src_dir$1'/'$file $des_dir$1
    done
}

for dir_f in `ls $src_dir`; do
    # echo $dir_f
    if [[ -d $src_dir$dir_f ]]; then
        if [[ ! -d $des_dir$dir_f ]] ; then
            mkdir $des_dir$dir_f
            echo 'Creating Dir:' $dir_f
        fi
        gen_dir $dir_f
    fi
done