#!/bin/bash

set -x 

source loadDDH.sh

# Extract gz file

#cp /nobackup/forsk/sm_terva/yopp/ddh_output/2018/03/06/00/DHFDLHARM.tar.gz .
#tar -xvf DHFDLHARM.tar.gz
cd /home/sm_marka/DDH/2018/02/02/
domains='1 2 3'

for D in ${domains}; do

# time step 100
mmmm="0100"

# Extract domains
  echo ddht -cEXTRAIT_DOMAIN -1DHFDLHARM+$mmmm -sDHFDLHARM+$mmmm.domain$D -E$D
  ddht -cEXTRAIT_DOMAIN -1DHFDLHARM+$mmmm -sDHFDLHARM+$mmmm.domain$D -E$D

# Make profiles
  echo ddhi DHFDLHARM+$mmmm.domain$D -lmylist
  ddhi DHFDLHARM+$mmmm.domain$D -lmylist

# Make budgets
  echo ddhb -v AA/CT -i DHFDLHARM+$mmmm.domain$D
  ddhb -v harmonie/CT -i DHFDLHARM+$mmmm.domain$D



# other time steps

# limit=1440
# step=60
# 
# i=60; while [ $i -le $limit ]; do
#   echo $i
# 
#   if [ $i -lt 100 ]
#   then
#    #echo Hey that\'s a 2-digit number.
#    mmmm="00"$i
#   else
#    if [ $i -lt 1000 ]
#    then
#      #echo Hey that\'s a 3-digit number.
#      mmmm="0"$i
#    else
#      #echo Hey that\'s 4-digit number.
#      mmmm=$i
#    fi
#   fi
# 
# # Extract domains
#   echo ddht -cEXTRAIT_DOMAIN -1DHFDLHARM+$mmmm -sDHFDLHARM+$mmmm.domain$D -E$D
#   ddht -cEXTRAIT_DOMAIN -1DHFDLHARM+$mmmm -sDHFDLHARM+$mmmm.domain$D -E$D
# 
# # Make profiles
#   echo ddhi DHFDLHARM+$mmmm.domain$D -lmylist
#   ddhi DHFDLHARM+$mmmm.domain$D -lmylist
# 
# # Make budgets
#   echo ddhb -v harmonie/CT -i DHFDLHARM+$mmmm.domain$D
#   ddhb -v harmonie/CT -i DHFDLHARM+$mmmm.domain$D
# 
#   i=$(($i + $step))
# done
# done
# 
# # Extract domains
# 
