#! /bin/bash

rm -f cscope.files  cscope.in.out  cscope.out  cscope.po.out  tags
PWD=`pwd`
#find $PWD -name "*.h" -o -name "*.c" -o -name "*.cc" -o -name "*.hxx" -o -name "*.cxx" -o -name "*.cpp" >cscope.files
find $PWD -regextype posix-extended -regex ".*\.(h|c|cc|hxx|cxx|cpp)$" > cscope.files
cscope -bq -i cscope.files
ctags -R --sort=yes --c++-kinds=+plx --c-kinds=+plx --fields=+iaS --extra=+q -I__wur -I__THROW $PWD
