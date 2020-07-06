![TimeSlide](./imgs/logo.png)

__a super-simple gui to slide old photographs into TODAY__

TimeSlide is a prototype concept to balance the ease of applying machine-learning "de-oldifying" (colorizing and, eventually, up-sampling) of old photographs without having to possess coding expertise or uploading your photographs to an online service. It is inspired by my desire to provide an easy-to-use offline option for my mother with her older family and ancestral photos. The name is derived from the title of an episode of the amazing British sitcom, "[Red Dwarf](https://www.reddwarf.co.uk/news/index.cfm)," wherein [timeslides](https://en.wikipedia.org/wiki/Timeslides) provided much more interactive features of old photographs.

TimeSlide is just pretty packaging (or an attempt of it). The hard work is by the [deoldify](https://github.com/jantic/DeOldify) project, torch developers, tkinter developers, and all the other enabling technologies.

## Setup

In macOS, ensure you have a [homebrew](https://brew.sh)ed version of Python 3.7 installed (*not* 3.8) and linked in your path, then run the bootstrap file which will clone deoldify, download the colorizing models, and install all python requirements in a virtual environment.

```
source bootstrap.sh
```

## Run

After activating the python virtual environment, simply run the python script.

```
python timeslide.py
```

## Bundle

Double check the file `timeslide.spec` in case any paths require modification. Then, in macOS, run

```
source bundle.sh
```

## Running the Bundled MacOS App

Please note that distributing the application to others will require that they enable unidentified developer apps to run. This can be done in the following way by providing those users with the following instructions.

1. Press COMMAND + SPACEBAR
2. Type `term`. When the Termina.app shows, click it (or hit ENTER).
3. In the window, type `sudo spctl --master-disable` (Please note double hypens before `master`.)
4. Enter password as required.
5. Open System Preferences.
6. Click "Security and Privacy." Make sure you're on the "General" tab.
7. Click the lock at the bottom left, and enter password.
8. Under "Allow apps downloaded from," ensure the "Anywhere" is selected.
9. Close System Preferences and double click the TimeSlide app to run.

## Useful Links

If you don't immediately have old black-and-white photos but want to test TimeSlide, here are some useful websites:

- [the way we were](https://www.reddit.com/r/TheWayWeWere/)
- [library of congress free-to-use](https://www.loc.gov/free-to-use/)

## Notes

- timeslide is very preliminary; lots of ideas on features to add
- image size and aspect ratio in window are just for display; the saved image will be correct resolution and proportions
- tested so far only on macOS, Python 3.7 installed with [homebrew](https://brew.sh)