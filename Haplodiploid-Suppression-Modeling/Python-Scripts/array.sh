#!/bin/bash
mkdir -p data
python3 panmictic.py -embryores 0.00 > data/1.part &
python3 panmictic.py -embryores 0.05 > data/2.part &
python3 panmictic.py -embryores 0.10 > data/3.part &
python3 panmictic.py -embryores 0.15 > data/4.part &
python3 panmictic.py -embryores 0.20 > data/5.part &
python3 panmictic.py -embryores 0.25 > data/6.part &
python3 panmictic.py -embryores 0.30 > data/7.part &
python3 panmictic.py -embryores 0.35 > data/8.part &
python3 panmictic.py -embryores 0.40 > data/9.part &
python3 panmictic.py -embryores 0.45 > data/10.part &
python3 panmictic.py -embryores 0.50 > data/11.part &
python3 panmictic.py -embryores 0.55 > data/12.part &
python3 panmictic.py -embryores 0.60 > data/13.part &
python3 panmictic.py -embryores 0.65 > data/14.part &
python3 panmictic.py -embryores 0.70 > data/15.part &
python3 panmictic.py -embryores 0.75 > data/16.part &
python3 panmictic.py -embryores 0.80 > data/17.part &
python3 panmictic.py -embryores 0.85 > data/18.part &
python3 panmictic.py -embryores 0.90 > data/19.part &
python3 panmictic.py -embryores 0.95 > data/20.part &
python3 panmictic.py -embryores 1.00 > data/21.part &
wait
cd data
cat *.part > array_data.csv
rm *.part
