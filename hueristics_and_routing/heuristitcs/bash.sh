#!/bin/bash

# Set the seed for both programs based on $RANDOM
SEED=$RANDOM
BUSES=3
PASSENGERS=4
run=1

for j in {1..5}
do
PASSENGERS=4
for i in {1..20}
do
    echo "Run $run"
    python oltea.py --seed $SEED --buses $BUSES --passengers $PASSENGERS --index $run
    python main.py --seed $SEED --buses $BUSES --passengers $PASSENGERS --index $run
    PASSENGERS=$((PASSENGERS+1))
    run=$((run+1))
done
BUSES=$((BUSES+1))
SEED=$RANDOM
done
