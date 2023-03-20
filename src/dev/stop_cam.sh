#!/bin/bash

# Calls a remote script with mandatory argument outputfilename.h264
# Also, a ssh config has to be set up on the host machine.
# Help function called if inputs are not ok
helpFunction()
{
   echo ""
   echo "Usage: $0 -p PID"
   echo -e "\t-i The viserpi to send SIGINT to (Ctrl-C)"
   exit 1 # Exit script after printing help
}

# Check if all inputs are ok
while getopts "i:" opt
do
   case "$opt" in
      i ) viserpi_num="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

# Print helpFunction in case parameters are empty
if [ -z "$viserpi_num" ]
then
   echo "You must specify which viserpi to stop, use '-i viserpi01' for example";
   helpFunction
fi

echo "Will send kill sig to $viserpi_num"

ssh $viserpi_num pid=$pid 'bash -s' <<'ENDSSH'
  # commands to run on remote host
  cd rise_camera/src/app
  #kill -SIGINT $pid
  pidn=$(<pidnum)
  echo $pidn
  kill -SIGINT $pidn
ENDSSH
