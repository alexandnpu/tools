#!/bin/bash

opt="-u"

accurev stat -fa -k | awk '{print $1}' | while read line; do
    if [[ `accurev stat -b $line` =~ "no such elem" ]]; then
       if [ ! -d $line ]; then
       /usr/bin/diff $opt /dev/null $line
       fi
    else
         accurev diff -j $line -- $opt
    fi
done

