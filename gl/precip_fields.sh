#!/usr/bin/env bash
#SBATCH --error=/home/ms/dk/nhd/scripts/sisaws/kristian_scripts/err_gl
#SBATCH --output=/home/ms/dk/nhd/scripts/sisaws/kristian_scripts/out_gl
#SBATCH --job-name=gl

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
D1=1
D2=20
#YEAR=1997
#MONTH=09
NL=$CLD/full_nam_prec

#for DAY in `seq -w 1 31`
#for DAY in 11 12 13 14 15 16 17 18 19 20
for DAY in `seq -w $D1 $D2`
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
      #DESTFILE=$DESTDIR/ICMSHFULL+000${H}.sfx
      #[ ! -f $FILE ] && ecp $EXPdir/$tdir/ICMSHFULL+000${H}.sfx $DESTFILE
      #$HOME/bin/gl -p $DESTFILE -n $sNL -o $DESTDIR/ICMSHFULL+000${H}_$EXP.grib 
      DESTDIR=$DS/$EXP/$tdir
      [ ! -d $DESTDIR ] && mkdir -p $DESTDIR
     for HH in `seq -w 03 06`;do
      FILE=$DESTDIR/ICMSHHARM+00${HH}
      [ ! -f $FILE  ] && ecp $EXPdir/$tdir/ICMSHHARM+00${HH} $FILE
      $HOME/bin/gl -p $FILE -n $NL -o $DESTDIR/PRECIP+00${HH}_$EXP.grib && rm -f $FILE
     done
    done

  done
done
exit 0
