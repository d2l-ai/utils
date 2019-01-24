#!/bin/bash

replace_with_space() {
	for f in $1/chapter*/*html; do
		sed -i s/Ⓐ/\ /g $f
	done
}

"$@"
