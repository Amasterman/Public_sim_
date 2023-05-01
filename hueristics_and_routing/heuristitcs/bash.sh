#!/bin/bash

# Set the seed for both programs based on $RANDOM
SEED=$RANDOM
BUSES=40
run=1

for j in {1..10}
do
PASSENGERS=$((2*BUSES))
for i in {1..2}
do
    echo "Run $run"
    python first.py --seed $SEED --buses $BUSES --passengers $PASSENGERS --stops 5000 --index $run
    python greedy.py --seed $SEED --buses $BUSES --passengers $PASSENGERS --stops 5000 --index $run
    PASSENGERS=$((PASSENGERS+3*BUSES))
    run=$((run+1))
done
BUSES=$((BUSES+6))
SEED=$RANDOM
done
