#!/bin/sh

SCRIPT=/usr/local/telstra-sms/server.py
PIDFILE=/var/run/telstra-sms.pid

# Start telstra-sms client
telstrasms_start() {
  echo "Starting telstra-sms daemon"

  EXISTPID=$(ps | grep $SCRIPT | grep -v grep | cut -d ' ' -f1)
  if [ -n "$EXISTPID" ]; then
    echo "telstra-sms daemon start fail, exisiting PID $EXISTPID"
    return 1
  fi

	PID=$($SCRIPT -d > /dev/null 2>&1 & echo $!)
	if [ -z $PID ]; then
	  echo "telstra-sms daemon start fail"
	else
    echo $PID > $PIDFILE
    echo "pid is $PID"
		echo "telstra-sms daemon started"
	fi
}


# Stop telstra-sms client
telstrasms_stop() {

	if [ -f "$PIDFILE" ] ; then
    echo "telstra-sms daemon still running, force kill"
    PID=$(cat $PIDFILE)
    kill -9 $PID
		rm -f $PIDFILE
  else
    echo "$PIDFILE file not found"
	fi
  echo "telstra-sms stopped"
}


case "$1" in
'start')
	telstrasms_start
	;;
'stop')
	telstrasms_stop
	;;
'restart')
	telstrasms_stop
  telstrasms_start
	;;
'status')
  if [ -f "$PIDFILE" ] ; then
    PID=$(cat $PIDFILE)
    if [ -n "`ps | grep $PID | grep -v 'grep' | cut -d ' ' -f1`" ]; then
      echo "Process dead but pid file exist"
    else
      echo "telstra-sms is running - Pid : $PID"
    fi
	else
		echo "telstra-sms is not running"
	fi
	;;
*)
echo "Usage $0 { start | stop | restart | status }"
exit 1
;;
esac
