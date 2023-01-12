#!/usr/bin/env bash
BINPATH=/scratch/ms/dk/nhd/DDH/ddhtoolbox/tools
DATAPATH=/scratch/ms/dk/nhd/SISAWS

#for bin in `ls -1 $BINPATH/ddh?`;do
#$bin
#done
#$BINPATH/ddhb  $DATAPATH/ICMSHHARM+0000
domains='1 2 3'
mmmm="0100"
for D in ${domains}; do

# time step 100

# Extract domains
  echo ddht -cEXTRAIT_DOMAIN -1DHFDLHARM+$mmmm -sDHFDLHARM+$mmmm.domain$D -E$D
  $BINPATH/ddht -cEXTRAIT_DOMAIN -1DHFDLHARM+$mmmm -sDHFDLHARM+$mmmm.domain$D -E$D
done
