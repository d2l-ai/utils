#!/bin/bash

DIR="build/_build/html"

for f in $DIR/chapter*/*html; do
	sed -i s/Ⓐ/\ /g $f
done

sed -i s/\<title\>《动手学深度学习》\ \&\#8212\;\ 《动手学深度学习》\ \ 文档\<\\\/title\>/\<title\>《动手学深度学习》\ \\\&\#8212\;\ 面向中文读者、能运行、可讨论\<\\\/title\>/g $DIR/index.html

