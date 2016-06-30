#!/bin/bash

cd `dirname $0`

###########################################################################

GOLD_STANDARDS=$(cd gold_standard; ls *.txt | sed -e 's/.txt//g' | sort)
VERSION=1.0

###########################################################################

IMPL=impl/cluster_one-${VERSION}.jar
PYTHON=`which python`
JAVA=`which java`
echo "Using ClusterONE ${VERSION}..."
echo ""


dataset="datasets/*.txt"
# for dataset in datasets/*.txt; do
	# echo `basename $dataset .txt`
	for GOLD_STANDARD in ${GOLD_STANDARDS}; do
    	# echo "Using gold standard: ${GOLD_STANDARD}"
    	echo $1
		i=1
    	# dataset="biogrid_yeast_physical_unweighted.txt"

	    ${JAVA} -jar ${IMPL} $dataset -d $1 >./results/CL1_results$1.txt #2>/dev/null
	    ${PYTHON} scripts/match_standalone.py -q -n ${dataset} \
		    -m frac -m cws -m ppv -m acc -m mmr \
		    gold_standard/${GOLD_STANDARD}.txt ./results/results$i.txt | awk '{ printf "  "; print $0 }'
	    echo ""
	    i=$((i+1))
	    # rm results.txt
	done
# done
