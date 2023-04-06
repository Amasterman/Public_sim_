#!/bin/bash

# Set the seed for both programs based on $RANDOM
SEED=$RANDOM
echo $SEED
for i in {1..2}
do
    # echo "s"
    python oltea.py --seed $SEED
    python main.py --seed $SEED

# 
    # ((SEED++))
done
# echo $?