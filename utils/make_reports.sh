#!/usr/bin/env bash

# Creates reports of drawed plots by merging them into a single PDF file per category

# if not arguments specified take default dir
if [[ $# -eq 0 ]] ; then
    TARGET_DIR=80_035_2_agr
else
    TARGET_DIR=${1}
fi

TARGET_DIR=../results/${TARGET_DIR}/plots
cd ${TARGET_DIR}
echo "Going to create reports for ${PWD}..."

cd crossover
echo "Creating report for crossover..."
convert *.png crossover_report.pdf
cd ..

cd mutation
echo "Creating report for mutation..."
convert *.png mutation_report.pdf
cd ..

cd population_size
echo "Creating report for population size..."
convert *.png population_report.pdf
cd ..

cd selection
echo "Creating report for selection..."
convert *.png selection_report.pdf
cd ..

mkdir -p reports
cd reports
echo "Copying reports to ${PWD}"
cp ../crossover/crossover_report.pdf .
cp ../mutation/mutation_report.pdf .
cp ../population_size/population_report.pdf .
cp ../selection/selection_report.pdf .
