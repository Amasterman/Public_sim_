#!/bin/bash

# Number of tests to run with different random seeds
SEED_REPEATS=3

# Set the initial seed and buses
BUSES=2
run=1

for j in {1..10}  # Change the range to adjust the number of test iterations
do
    PASSENGERS=$((2*BUSES))
    for i in {1..2}
    do
        # Test with different number of stops
        for STOPS in 500 2500 5000
        do
            # Test with different random seeds
            for seed_repeat in $(seq 1 $SEED_REPEATS)
            do
                SEED=$RANDOM
                echo "Run $run"
                python first.py --seed $SEED --buses $BUSES --passengers $PASSENGERS --stops $STOPS --index $run
                python greedy.py --seed $SEED --buses $BUSES --passengers $PASSENGERS --stops $STOPS --index $run
                run=$((run+1))
            done
        done

        PASSENGERS=$((PASSENGERS+3*BUSES))
    done
    BUSES=$((BUSES+4))
done