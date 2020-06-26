![TimeSlide](./imgs/logo.png)

__a super-simple gui to slide old photographs into TODAY__

TimeSlide is a prototype application concept to balance the ease of applying machine-learning "de-oldifying" (colorizing and up-sampling) of old photographs without having to possess coding expertise or uploading your photographs to an online service. It is inspired by my desire to provide an easy-to-use offline option for my mother with her older family photos. The name is derived from the title of an episode of the amazing British sitcom, "[Red Dwarf](https://www.reddwarf.co.uk/news/index.cfm)," wherein [timeslides](https://en.wikipedia.org/wiki/Timeslides) provided much more interactive features of old photographs.

TimeSlide is just pretty packaging (or an attempt of it). The hard work is by the [deoldify](https://github.com/jantic/DeOldify) project, torch developers, tkinter developers, and all the other enabling technologies.

## Setup

In macOS, ensure you have a [homebrew](https://brew.sh)ed version of Python 3.7 installed (*not* 3.8) and linked in your path, then run the bootstrap file which will clone deoldify, download the colorizing models, and install all python requirements in a virtual environment.

```
source bootstrap.sh
```

## Run

Just run the python script

```
python timeslide.py
```

## Bundle

Double check the file `timeslide.spec` in case any paths require modification. Then, in macOS, run

```
source bundle.sh
```

## Useful Links

If you don't immediately have old black-and-white photos but want to test TimeSlide, here are some useful websites:

- [the way we were](https://www.reddit.com/r/TheWayWeWere/)
- [library of congress free-to-use](https://www.loc.gov/free-to-use/)

## Notes

- timeslide is very preliminary; lots of ideas on features to add
- image size and aspect ratio in window are just for display; the saved image will be correct resolution and proportions
- tested so far only on macOS, Python 3.7 installed with [homebrew](https://brew.sh)