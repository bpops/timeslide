![TimeSlide](./imgs/logo.png)

__a super-simple gui to slide old photographs into TODAY__

TimeSlide is a prototype concept to balance the ease of applying machine-learning colorizing--and eventually, up-sampling--of old photographs without having to possess coding expertise or uploading your photographs to an online service. It is inspired by my desire to provide an easy-to-use *offline* option for my mother with her older family and ancestral photos. The app name is derived from the title of an episode of the amazing British sitcom, "[Red Dwarf](https://www.reddwarf.co.uk/news/index.cfm)," wherein [timeslides](https://en.wikipedia.org/wiki/Timeslides) provided much more interactive features of old photographs.

TimeSlide is just pretty packaging (or an attempt of it, I'm a newb). The hard work is by the [deoldify](https://github.com/jantic/DeOldify) project, torch developers, tkinter developers, and all the other enabling technologies provided by selfless contributors to both the open source and free software communities. 

__Importantly, TimeSlide targets macOS.__ Currently, since it is based solely on python modules, you could certainly bundle a Windows application. But no support on that procedure is provided herein (though you're welcome to figure it out yourself and submit a PR).

## Setup for Development

In macOS, install [homebrew](https://brew.sh). Then, use it to install Python 3.7 (*not* 3.8, since Pyinstaller is not compatible) with `brew install python3`. Link it in your path (`brew link python3`; might not be necessary).

Ensure that your `python` command is correctly linked to the homebrew version:
``realpath `which python` ``.

Also verify here that it is python 3.7, or else just run `python --version` to confirm.

Next, run the bootstrap file which will clone deoldify, download the colorizing models, and install all python requirements in a virtual environment.
```
source bootstrap.sh
```

## Execute TimeSlide for Development

After activating the python virtual environment (`source venv/bin/activate`), simply run the python script:
```
python timeslide.py
```

## Bundle for macOS

Since the whole point of TimeSlide is ease of use, we require a solution for bundling the app that can be distributed to others. To do this, first open the file `timeslide.spec` and ensure that the path to your homebrew (Cellar'ed) version of `libpng16.16.dylib` is correct (slight modifications may be necessary depending on version number.) 

Next, in terminal, run:
```
source bundle.sh
```

With this, pyinstaller will bundle the app, including all necessary python modules and dynamic libraries. It will be bundled into a single `.app` bundle (as well as a binary executable) under the `dist` folder. Additionally, the bash script will copy over the icon files into the `.app` file.

We recommend you then compress the `.app` file into a zip file before sharing via file-sharing services, e.g., [iCloud](https://www.icloud.com) or [DropBox](https://www.dropbox.com).

## Running the Bundled macOS App

Please note that distributing the application to others will require that they enable unidentified developer apps to run on any somewhat recent version of macOS. This can be done by providing those users with the following instructions.

1. Press `⌘` + `SPACEBAR`.
2. Type `term`. When the Terminal.app shows, click it (or hit `ENTER`).
3. In the window, type `sudo spctl --master-disable` (note double hyphens before `master`), hit `ENTER`.
4. Enter password as required, hit `ENTER`.
5. Open System Preferences.
6. Click "Security and Privacy." Make sure you're on the "General" tab.
7. Click the lock at the bottom left, and enter password.
8. Under "Allow apps downloaded from," ensure that "Anywhere" is selected.
9. Close System Preferences and double-click the TimeSlide app to run.

## Release Notes

### v0.1 (2020.06.08)

- first working version
- colorize-capable (and optional)
- render factor selection on colorize
- load from local file or url
- gui layout to guide user

### v0.2 (2020.07.05)

- `.jpg` now default when saving
- status updates now provided during procedure
- tooltips now help guide user
- blurry text in macOS resolved
- dedicated icon
- stable model + artistic model both included
- app can now be fully bundled for macOS

### v0.3 (in progress)

...

## Useful Links

If you just want to test out TimeSlide but don't have black-and-white photos available, here are some nice resources:

- [the way we were](https://www.reddit.com/r/TheWayWeWere/)
- [library of congress free-to-use](https://www.loc.gov/free-to-use/)
- [pexels: black and white](https://www.pexels.com/search/black%20and%20white/)

## (Current) Additional Notes

- TimeSlide is very preliminary; lots of ideas on features to add.
- Image size and aspect ratio in window are just for display; the saved image will be correct resolution and proportions.
- Tested so far only on macOS Catalina (10.15.5), Python 3.7 installed with [homebrew](https://brew.sh).
- URL loading has known bugs. Load from file preferred.