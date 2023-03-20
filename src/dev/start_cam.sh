#!/bin/bash
# Calls a remote script with mandatory argument outputfilename.h264
# Also, a ssh config has to be set up on the host machine.

# Help function called if inputs are not ok
helpFunction()
{
   echo ""
   echo "Usage: $0 -o filename.h264 -d duration_in_seconds"
   echo -e "\t-o Output filemname ending in .h264"
   echo -e "\t-d Duration in seconds"
   echo -e "\t-i The Viserpi to start recording on"
   exit 1 # Exit script after printing help
}

# Check if all inputs are ok
while getopts "o:d:i:" opt
do
   case "$opt" in
      o ) output="$OPTARG" ;;
      d ) duration="$OPTARG" ;;
      i ) viserpi_num="$OPTARG";;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

# Print helpFunction in case parameters are empty
if [ -z "$output" ] || [ -z "$duration" ] || [ -z "$viserpi_num" ]
then
   echo "Some or all of the parameters are empty";
   helpFunction
fi

echo "Will record $duration seconds to filename $output on $viserpi_num."
echo "Stop recordeing in advance by issuing the stop stop_cam1 script specifying the same viserpi_num"

# Begin script in case all parameters are correct.
ssh $viserpi_num output=$output duration=$duration 'bash -s' <<'ENDSSH'
   # commands to run on remote host
   cd rise_camera/src/app
   # Start camera recording and note the pid-num for sending signals to process later
	python camera.py --output=$output --duration=$duration > /dev/null & echo $! > pidnum
ENDSSH

# Stand alone script with one arg = filename
# ssh viserpi01 ARG1="$1" 'bash -s' <<'ENDSSH'
#   # commands to run on remote host
#   cd rise_camera/src/app
# 	python camera.py --output=$ARG1
# ENDSSH
