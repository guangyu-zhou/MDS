#!/bin/bash

# cd `dirname $0`
# dataset=$1
###########################################################################

GOLD_STANDARDS=$(cd gold_standard; ls *.txt | sed -e 's/.txt//g' | sort)
# VERSION=0.93
VERSION = 1.0

###########################################################################

IMPL=impl/cluster_one-${VERSION}.jar
PYTHON=`which python`
JAVA=`which java`

# echo $dataset

echo "Using ClusterONE ${VERSION}..."
echo ""

for GOLD_STANDARD in ${GOLD_STANDARDS}; do
    echo "Using gold standard: ${GOLD_STANDARD}"
    echo ""

    for dataset in datasets/*.txt; do
    echo $dataset
    # dataset = "krogan2006_core.txt"
	    # echo `basename $dataset .txt`
			${PYTHON} scripts/match_standalone.py -q -n ${dataset} \
		    -m frac -m cws -m ppv -m acc -m mmr \
		    gold_standard/${GOLD_STANDARD}.txt gavin-result.txt | awk '{ printf "  "; print $0 }'
	    echo ""
	    # rm results.txt
	done
done
