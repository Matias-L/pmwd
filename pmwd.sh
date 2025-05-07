#!/bin/sh

#####
## PMWD: PMs Wet Dream. A simple tool for tasks time tracking.
####


# Check if base dir exists
DIR=~/pmwd
if [ ! -d "$DIR" ]; then
    mkdir ~/pmwd
fi

LOCKFILE=$DIR/.lock     # File used as flag to check if session is ongoing
RAWFILE=$DIR/raw.log    # File to save history of sessions
TIMEFILE=$DIR/time.csv  # Table with sessions durations
TIMETABLE=$DIR/timeTable.csv  # New table with sessions durations

# Create time table with corresponding format
if [ ! -f "$TIMETABLE" ]; then
    echo "Hora inicio,Descripcion inicio,Hora fin,Descripcion fin,H,M,S" >> $TIMETABLE
fi

# Check if "lock" file exist
# If true, then a session is in progress
if [ -f "$LOCKFILE" ]; then
    # Ending session
    endMessage=$(zenity --entry --text="Terminando sesion. Algo para mencionar?")
    answer=$? # 0: User pressed "Ok". 1: "cancel"
    
    if [ $answer -eq 0 ]
    then
        TASKSTARTINFO="$(tail -n 1 $RAWFILE)"
        TASKENDINFO="$(date),$endMessage"
        echo "$(date) || $endMessage" >> $RAWFILE    

        # Time table entry creation.
        prevTS=$(cat $LOCKFILE)
        newTS=$(date +%s)
        sessionTimeDiff=$(($newTS - $prevTS)) # Saved as UNIX timestamp

        registeredTime="$((sessionTimeDiff /60/60)) H,$(((sessionTimeDiff/60) % 60)) M,$(($sessionTimeDiff % 60)) S"
        echo "$endMessage, $registeredTime" >> $TIMEFILE

        echo "$TASKSTARTINFO, $TASKENDINFO, $registeredTime" >> $TIMETABLE
        rm $LOCKFILE # Remove this file so the session is over
        
        notify-send -t 3000 "Finalizada sesion - $registeredTime"
    else
        echo "Mentirita"
    fi
    
    else
    # Begin session
    concept=$(zenity --entry --text="Que tarea arrancas?")
    answer=$? # 0: User pressed "Ok". 1: "cancel"
    
    if [ $answer -eq 0 ]
    then
        notify-send -t 3000 "Empezaste $concept"
        timestamp=$(date +%s)
        echo $timestamp > $LOCKFILE
        echo "$(date),$concept" >> $RAWFILE
    else
        echo "Mentirita"
    fi


fi