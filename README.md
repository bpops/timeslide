# timeslide

__a beautifully simple gui to slide old photographs into TODAY__

Timeslide is a prototype concept for an application to balance the ease of applying machine-learning colorizing and "de-oldifying" photographs without having possess coding expertise or to upload your photographs to an online service. It is inspired by my desire to provide an easy-to-use offline option for my mother with her older family photos. The name is derived from the title of an episode of the wonderful British sitcom, "[Red Dwarf](https://www.reddwarf.co.uk/news/index.cfm)," wherein [timeslides](https://en.wikipedia.org/wiki/Timeslides) provided much more interactive features of old photographs.

Much thanks to all the hard work by the [deoldify](https://github.com/jantic/DeOldify) project.

## Setup

Run the bootstrap file which will clone deoldify, download the colorizing model, and install all python requirements (if you want to run in a virtual environment then you'll instead want to run these steps manually).

```
sh boot_strap.sh
```

## Run

Just run the python script

```
python timeslide.py
```

## Useful Links

- [the way we were](https://www.reddit.com/r/TheWayWeWere/)

## Notes

- timeslide is very preliminary; lots of ideas on features to add
- image size and aspect ratio in window are just for display; the saved image will be correct resolution and proportions
- tested so far only on macOS