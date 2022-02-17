#!/bin/sh

#####
## PMWD: PMs Wet Dream. A simple tool for tasks time tracking.
####


# Check if base dir exists
DIR=~/Documents/pmwd
if [ ! -d "$DIR" ]; then
    mkdir ~/Documents/pmwd
fi

LOCKFILE=$DIR/.lock     # File used as flag to check if session is ongoing
RAWFILE=$DIR/raw.log    # File to save history of sessions
TIMEFILE=$DIR/time.csv  # Table with sessions durations


# Check if "lock" file exist
# If true, then a session is in progress
if [ -f "$LOCKFILE" ]; then
    # Ending session
    endMessage=$(zenity --entry --text="Terminando sesion. Algo para mencionar?")
    echo "$(date) || $endMessage" >> $RAWFILE
    

    # Time table entry creation.
    prevTS=$(cat $LOCKFILE)
    newTS=$(date +%s)
    sessionTimeDiff=$(($newTS - $prevTS)) # Saved as UNIX timestamp

    registeredTime="$((sessionTimeDiff /60/60)) H,$(((sessionTimeDiff/60) % 60)) M,$(($sessionTimeDiff % 60)) S"
    echo "$endMessage, $registeredTime" >> $TIMEFILE

    rm $LOCKFILE # Remove this file so the session is over
    
    notify-send -t 3000 "Finalizada sesion"

    else
    # Begin session
    concept=$(zenity --entry --text="Que tarea arrancas?")
    notify-send -t 3000 "Empezaste $concept"
    timestamp=$(date +%s)
    echo $timestamp > $LOCKFILE
    echo "$(date) -- $concept" >> $RAWFILE
fi