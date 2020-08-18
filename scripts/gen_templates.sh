#!/usr/bin/env bash

set -eu

cd $(dirname ${BASH_SOURCE})/../src/vulnpy/templates/fragments

for fragment in *.frag.html; do
	pagename=${fragment%.frag.html}.html
	outfilename=../$pagename
	echo "<!-- This file was automatically generated. Do not edit manually. -->" > ${outfilename}
	sed -e "/###vulnpy-injection-site###/r${fragment}" base.html >> ${outfilename}
	echo "wrote $pagename"
done
