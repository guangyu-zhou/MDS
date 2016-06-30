#!/bin/bash

# cd `dirname $0`
# dataset=$1
###########################################################################

GOLD_STANDARDS=$(cd gold_standard; ls *.txt | sed -e 's/.txt//g' | sort)
# VERSION=0.93
VERSION=1.0
echo $GOLD_STANDARDS
###########################################################################

IMPL=impl/cluster_one-${VERSION}.jar
PYTHON=`which python`
JAVA=`which java`

# echo $dataset

echo "Using ClusterONE ${VERSION}..."
echo ""
dataset="datasets/*.txt"
# dataset="datasets/gavin2006_socioaffinities_rescaled.txt"
# dataset="datasets/collins2007.txt"
# dataset="datasets/krogan2006_core.txt"
# dataset="datasets/krogan2006_extended.txt"

echo $dataset
# wc -l bioGrid-result.txt 
for mds in cur/*.txt; do
    echo $mds

	for GOLD_STANDARD in ${GOLD_STANDARDS}; do
    	echo "Using gold standard: ${GOLD_STANDARD}"
    	echo ""

	    echo `basename $dataset .txt`
		${PYTHON} scripts/match_standalone.py -q -n ${dataset} \
		-m frac -m cws -m ppv -m acc -m mmr \
		gold_standard/${GOLD_STANDARD}.txt $mds | awk '{ printf "  "; print $0 }'
		echo ""
	    # rm results.txt
	done
done
