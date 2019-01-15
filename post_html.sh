#!/bin/bash

DIR="build/_build/html"

for f in $DIR/chapter*/*html; do
	sed -i s/Ⓐ/\ /g $f
done

sed -i s/\<title\>Dive\ into\ Deep\ Learning\ \&\#8212\;\ Dive\ into\ Deep\ Learning\ \ documentation\<\\\/title\>/\<title\>Dive\ into\ Deep\ Learning\ \\\&\#8212\;\ An\ Interactive\ Deep\ Learning\ Book\<\\\/title\>/g $DIR/index.html

