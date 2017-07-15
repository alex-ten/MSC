#!/bin/bash

MODEL_NAME='tiny_'

for i in {1..3};
do
    NAME=$MODEL_NAME$i
    python3.5 trainer.py --name=$NAME --train_data='tiny_data' --save_as=$NAME
done    
        


