if [ -f /var/run/reboot-required ]; 
  then
    /bin/python3 /jenkins/patching/selfStatusUpdate.py 1
  else
    /bin/python3 /jenkins/patching/selfStatusUpdate.py 0
fi