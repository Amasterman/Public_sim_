#!/bin/bash

# Set the seed for both programs based on $RANDOM
SEED=$RANDOM
BUSES=2
run=1

for j in {1..10}
do
PASSENGERS=$BUSES
for i in {1..5}
do
    echo "Run $run"
    python oltea.py --seed $SEED --buses $BUSES --passengers $PASSENGERS --stops 5000 --index $run
    python greedy.py --seed $SEED --buses $BUSES --passengers $PASSENGERS --stops 5000 --index $run
    PASSENGERS=$((PASSENGERS+6))
    run=$((run+1))
done
BUSES=$((BUSES+5))
SEED=$RANDOM
done
