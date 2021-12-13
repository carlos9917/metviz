#!/usr/bin/env bash
VAR="Rain"
TEST="test"
DATE="2021081412"
F1=figures/ref_Temperature_2021081412.png
F2=figures/test_Temperature_2021081412.png
F3=figures/diff_Temperature_2021081412.png

F1=hourly_test_Rain_0003_0004_2021081412.png
F2=hourly_test_Rain_0004_0005_2021081412.png
F3=hourly_test_Rain_0005_0006_2021081412.png


module load python3
python3 combine_images.py -figs $F1,$F2,$F3  -fout ${TEST}_${VAR}_${DATE}.png


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
