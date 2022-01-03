#!/usr/bin/env bash
VAR="Rain"
TEST="ref"
DATE="2021081412"
F1=figures/ref_Temperature_2021081412.png
F2=figures/test_Temperature_2021081412.png
F3=figures/diff_Temperature_2021081412.png

F1=hourly_test_Rain_0003_0004_2021081412.png
F2=hourly_test_Rain_0004_0005_2021081412.png
F3=hourly_test_Rain_0005_0006_2021081412.png


module load python3
#python3 combine_images.py -figs $F1,$F2,$F3  -fout ${TEST}_${VAR}_${DATE}.png

function loop_dates()
{
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
    for HOUR in `seq -w 0 3 21`;do
      DATE=${YEAR}${MONTH}${DAY}${HOUR}
     F1=figures/${TEST}/hourly_${TEST}_${VAR}_0003_0004_${DATE}.png
     F2=figures/${TEST}/hourly_${TEST}_${VAR}_0004_0005_${DATE}.png
     F3=figures/${TEST}/hourly_${TEST}_${VAR}_0005_0006_${DATE}.png
     FOUT=figures/${TEST}/${TEST}_${VAR}_${DATE}.png
     echo "Combining $F1 $F2 $F3"
     python3 combine_images.py -figs $F1,$F2,$F3  -fout ${FOUT}
    done
  done
  done
}

loop_dates

#convert ref_${VAR}_${DATE}.png -trim ref.png
#convert test_${VAR}_${DATE}.png test.png
#convert diff_${VAR}_${DATE}.png diff.png
#convert +append ref.png test.png diff.png ${VAR}_${DATE}.png
##convert out.png -pointsize 30 -gravity North -background White -splice 0x42 -annotate +10+20 "Temperature for test,ref and difference (left to right). Forecast starting on 2021081412" ${VAR}_${DATE}.png
#rm ref.png
#rm test.png
#rm diff.png
#exit
#
#if [ $VAR == "Rain" ]; then
#    F1=diff_${TEST}_0003_0004_Rain_2021081412_cropped.png
#    F2=diff_${TEST}_0004_0005_Rain_2021081412_cropped.png
#    F3=diff_${TEST}_0005_0006_Rain_2021081412_cropped.png
#    FINAL=${TEST}_HourlyRainDiffs_3_6_$DATE.png
#    
#    convert +append $F1 $F2 $F3 out.png
#    #convert $FINAL -title "TEST" test.png
#    
#    convert out.png -pointsize 30 -gravity North -background White -splice 0x42 -annotate +200+20 "Ref run: hourly rain differences for hours 3-4,4-5,5-6 (left to right). Forecast start: 2021081412" $FINAL
#    rm out.png
#fi
#
