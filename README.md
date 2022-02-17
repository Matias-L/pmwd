# PMWD
## A simple tool for time tracking.

Want to make your PMs happy? Keep track of your tasks duration with a simple key binding.

## Instalation
* Clone this repo wherever you want.
* Add execution permissions to the script with `sudo chmod u+x pmwd.sh`
* Add a key binding. For example, with Xubuntu, go to `settings -> keywoard -> Application shortcuts -> add`

And you are done! Executing the key binging once will ask for a session name and then start time tracking. Executing the key binding again will stop the session and will let you add a small description of the work done.


## Files & folders

A folder `pmwd` will be created inside the `~/Documents` directory.
Here your time will be tracked in two files:
1. raw.log: Each time you execute the key binding an entry will be registered with timestamp and message.
2. time.csv: Each time you end a session, an entry with the ending message and time of session will be created.

## Contribution

Feel free to make a PR if you feel like adding a change.

## Licence

Distributed under _beerware_ licence. So, if you find this tool usefull and happen to stumble with me IRL, you know ;)
