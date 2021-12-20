#!/bin/bash
#SBATCH --error=/home/ms/dk/nhd/scripts/sisaws/kristian_scripts/err_gl2
#SBATCH --output=/home/ms/dk/nhd/scripts/sisaws/kristian_scripts/out_gl2
#SBATCH --job-name=gl_all


CLD=$PWD #$HOME/scr/IGB_exps
LDS=$SCRATCH/SISAWS/IGB/tmp
DS=$SCRATCH/SISAWS/IGB/data
FS=$SCRATCH/SISAWS/IGB/figures
#glbin=
[ ! -d $LDS ] && mkdir -p $LDS
[ ! -d $DS ] && mkdir -p $DS
[ ! -d $FS ] && mkdir -p $FS
#EXP1dir=ectmp:/nhe/harmonie/carra_20180703_2012
#EXP1=IGB_201207_alpha2
#EXP1dir=ectmp:/nhx/harmonie/beta1_IGB_2012
#EXP1=IGB_201207_beta1
#EXP1dir=ec:/nhx/harmonie/beta2_IGB_2012_1
#EXP1=beta2_IGB_2012_1
#EXP1dir=ectmp:/nhz/harmonie/2012_beta2_IGB_promice
#EXP1=IGB_beta2_no_promice
EXP1dir=ec:/nhp/harmonie/IGB_S3_ref
EXP1=IGB_S3_ref
#EXP2dir=ectmp:/nhe/harmonie/carra_20180703_2012_gcnet
#EXP2=IGB_gcnet
#EXPstr=expts_IGB_gcnet
#diffstr=diff_IGB_gcnet
#EXP2dir=ectmp:/nhp/harmonie/IGB_MOD_test
#EXP2=IGB_MOD_test
#EXPstr=expts_IGB_MOD_test
#diffstr=diff_IGB_MOD_test
#EXP2dir=ec:/nhe/harmonie/beta2_IGB_2012
#EXP2=IGB_beta2
EXP2dir=ec:/nhp/harmonie/IGB_S3_test
EXP2=IGB_S3_test
EXPstr=expts_IGB_S3SICE
#diffstr=diff_IGB_beta2
#diffstr=diff_IGB_beta2_promice
diffstr=diff_IGB_S3SICE
#EXP2dir=ectmp:/nhp/harmonie/igb_MOD_bc
#EXP2=igb_MOD_bc
#EXPstr=expts_IGB_bias_corr_MOD
#diffstr=diff_IGB_bias_corr_MOD
#EXP2dir=ectmp:/nhx/harmonie/2012_beta2_IGB_msnow/
#EXP2=igb_msnow
#EXPstr=expts_IGB_msnow
#diffstr=diff_IGB_msnow
YEAR=2021
MONTH=08
#YEAR=1997
#MONTH=09
sNL=$CLD/sfx_nam
NL=$CLD/full_nam
npar=`head -n 2 $NL | tail -n 1 | wc | awk '{print ($3-17)/4}'`
surf_npar=`head -n 2 $sNL | tail -n 1 | wc | awk '{print ($3-17)/4}'`
tpar=`expr $npar + $surf_npar`

#for DAY in `seq -w 1 31`
#for DAY in 11 12 13 14 15 16 17 18 19 20
for DAY in 14 14
do
  for HOUR in `seq -w 0 3 21`
  #for HOUR in 12
  do
    tdir=$YEAR/$MONTH/$DAY/$HOUR
    DATA=$DS/$tdir
    #[ -e $DATA ] || mkdir -p $DATA
    for EXPdir in $EXP1dir $EXP2dir
    do
      [ "$EXPdir" = "$EXP1dir" ] && EXP=$EXP1
      [ "$EXPdir" = "$EXP2dir" ] && EXP=$EXP2
      FILE=$EXPdir/$tdir/ICMSHFULL+0003.sfx
      DESTDIR=$DS/$EXP/$tdir
      [ ! -d $DESTDIR ] && mkdir -p $DESTDIR
      DESTFILE=$DESTDIR/ICMSHFULL+0003.sfx
      [ ! -f $FILE ] && ecp $EXPdir/$tdir/ICMSHFULL+0003.sfx $DESTFILE
      $HOME/bin/gl -p $DESTFILE -n $sNL -o $DESTDIR/ICMSHFULL+0003_$EXP.grib && rm -f $DESTFILE

      DESTDIR=$DS/$EXP/$tdir
      [ ! -d $DESTDIR ] && mkdir -p $DESTDIR
      DESTFILE=$DESTDIR/ICMSHHARM+0003
      [ ! -f $FILE  ] && ecp $EXPdir/$tdir/ICMSHHARM+0003 $DESTFILE
      $HOME/bin/gl -p $DESTFILE -n $NL -o $DESTDIR/ICMSHHARM+0003_$EXP.grib && rm -f $DESTFILE
    done
    #mkdir $LDS/$EXP1
    #mkdir $LDS/$EXP2
    #exp_list=''
    #for par in `seq 1 $surf_npar`
    #do
    #  for EXPdir in $EXP1dir $EXP2dir
    #  do
    #    [ $EXPdir = $EXP1dir ] && EXP=$EXP1
    #    [ $EXPdir = $EXP2dir ] && EXP=$EXP2
    #    cd $CLD/tmp
    #    wgrib -d $par -text $LDS/ICMSHFULL+0003_$EXP.grib
    #    cd $CLD
    #    $CLD/line_add.x && rm $CLD/tmp/dump
    #    mv $CLD/tmp/ladump $LDS/$EXP/dump_$par.dat
    #  done
    #  /usr/bin/paste $LDS/$EXP1/dump_$par.dat $LDS/$EXP2/dump_$par.dat > $DATA/${EXPstr}_$par.dat && rm -f $LDS/$EXP1/dump_[0-9]*.dat && rm -f $LDS/$EXP2/dump_[0-9]*.dat
    #  exp_list=`echo $exp_list $DATA/${EXPstr}_${par}.dat`
    #done
    #for par in `seq 1 $npar`
    #do
    #  fpar=`expr $surf_npar + $par`
    #  for EXPdir in $EXP1dir $EXP2dir
    #  do
    #    [ $EXPdir = $EXP1dir ] && EXP=$EXP1
    #    [ $EXPdir = $EXP2dir ] && EXP=$EXP2
    #    [ -d $LDS/$EXP ] || mkdir -p $LDS/$EXP
    #    cd $CLD/tmp
    #    wgrib -d $par -text $LDS/ICMSHHARM+0003_$EXP.grib
    #    cd $CLD
    #    $CLD/line_add.x && rm $CLD/tmp/dump
    #    mv $CLD/tmp/ladump $LDS/$EXP/dump_$fpar.dat
    #  done
    #  /usr/bin/paste $LDS/$EXP1/dump_$fpar.dat $LDS/$EXP2/dump_$fpar.dat > $DATA/${EXPstr}_$fpar.dat && rm -f $LDS/$EXP1/dump_[0-9]*.dat && rm -f $LDS/$EXP2/dump_[0-9]*.dat
    #  exp_list=`echo $exp_list $DATA/${EXPstr}_${fpar}.dat`
    #done
    #rmdir $LDS/$EXP1
    #rmdir $LDS/$EXP2
    #rm -f $LDS/*.grib
    #/usr/bin/paste $exp_list > $DATA/${EXPstr}.dat && rm -f $DATA/${EXPstr}_[0-9]*.dat
    #awk '{ if ( $1 ~ /[0-9]/ ) print $2-$1, $4-$3, $6-$5, $8-$7, $10-$9, $12-$11, $14-$13, $16-$15, $18-$17, $20-$19, $22-$21, $24-$23, $26-$25, $28-$27, $30-$29, $32-$31, $34-$33, $36-$35, $38-$37, $40-$39, $42-$41, $44-$43, $46-$45, $48-$47, $50-$49, $52-$51, $54-$53, $56-$55, $58-$57, $60-$59, $62-$61, $64-$63, $66-$65, $68-$67 ; else print ; }' $DATA/${EXPstr}.dat > $DATA/$diffstr.dat
  done
done
exit 0
