#!/usr/bin/env bash
#SBATCH --error=/home/ms/dk/nhd/scripts/metviz/logs/err_plot
#SBATCH --output=/home/ms/dk/nhd/scripts/metviz/logs/out_plot
#SBATCH --job-name=plot

module load python3
YEAR=2021
MONTH=08
D1=11 #first 10 days are just spin up
D2=20
HOURS1=(0003 0004 0005)
HOURS2=(0004 0005 0006)
for i in 0 1 2 3; do
HOUR1=${HOURS1[i]}
HOUR2=${HOURS2[i]}
for DAY in `seq -w $D1 $D2`; do
  #for HOUR in `seq -w 0 3 21`;do
  for HOUR in 06; do
    DATE=$YEAR/$MONTH/$DAY/$HOUR
    echo $DATE $HOUR1 $HOUR2
    sed "s|REPLACETIME|$DATE|g;s/REPLACEHOUR1/$HOUR1/g;s/REPLACEHOUR2/$HOUR2/g" settings_temp.ini  > settings.ini
    python3 plot_surf_vars.py
    exit 0
  done
done
done
