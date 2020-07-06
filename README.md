![TimeSlide](./imgs/logo.png)

__a super-simple gui to slide old photographs into TODAY__

TimeSlide is a prototype concept to balance the ease of applying machine-learning "de-oldifying" (colorizing and, eventually, up-sampling) of old photographs without having to possess coding expertise or uploading your photographs to an online service. It is inspired by my desire to provide an easy-to-use offline option for my mother with her older family and ancestral photos. The name is derived from the title of an episode of the amazing British sitcom, "[Red Dwarf](https://www.reddwarf.co.uk/news/index.cfm)," wherein [timeslides](https://en.wikipedia.org/wiki/Timeslides) provided much more interactive features of old photographs.

TimeSlide is just pretty packaging (or an attempt of it). The hard work is by the [deoldify](https://github.com/jantic/DeOldify) project, torch developers, tkinter developers, and all the other enabling technologies.

## Setup for Development

In MacOS, install [homebrew](https://brew.sh). Then, use it to install Python 3.7 (*not* 3.8) with `brew install python3`. Ensure it is linked in your path (`brew link python3`). You can always double-check that this is the correct version: `python --version` should show 3.7. Next, run the bootstrap file which will clone deoldify, download the colorizing models, and install all python requirements in a virtual environment.

```
source bootstrap.sh
```

## Execute TimeSlide

After activating the python virtual environment (`source venv/bin/activate`), simply run the python script:
```
python timeslide.py
```

## Bundle for MacOS

Since the whole point of TimeSlide is ease of use, we require a solution for bundling the app that can be distributed to others. To do this, first open the file `timeslide.spec` and ensure that the path to your homebrew version (Cellar'ed) `libpng16.16.dylib` is correct (slight modifications may be necessary depending on version number.) 

Next, in terminal, run:
```
source bundle.sh
```

With this, pyinstaller will bundle the app, including all necessary python modules and dynamic libraries. It will be bundled into a single `.app` bundle (as well as a binary executable) under the `dist` folder. Additionally, the bash script will copy over the icon files into the `.app` file.

Recommend you then comporess the `.app` file into a zip file before sharing via file-sharing services, e.g., iCloud or DropBox.

## Running the Bundled MacOS App

Please note that distributing the application to others will require that they enable unidentified developer apps to run on any somewhat recent version of MacOS. This can be done by providing those users with the following instructions.

1. Press COMMAND + SPACEBAR.
2. Type `term`. When the Terminal.app shows, click it (or hit ENTER).
3. In the window, type `sudo spctl --master-disable` (note double hyphens before `master`.)
4. Enter password as required.
5. Open System Preferences.
6. Click "Security and Privacy." Make sure you're on the "General" tab.
7. Click the lock at the bottom left, and enter password.
8. Under "Allow apps downloaded from," ensure that "Anywhere" is selected.
9. Close System Preferences and double-click the TimeSlide app to run.

## Useful Links

If you don't immediately have old black-and-white photos but want to test TimeSlide, here are some useful websites:

- [the way we were](https://www.reddit.com/r/TheWayWeWere/)
- [library of congress free-to-use](https://www.loc.gov/free-to-use/)

## Notes

- TimeSlide is very preliminary; lots of ideas on features to add.
- Image size and aspect ratio in window are just for display; the saved image will be correct resolution and proportions.
- Tested so far only on MacOS Catalina (10.15.5), Python 3.7 installed with [homebrew](https://brew.sh)
- URL loading has known bugs. Load from file preferred.