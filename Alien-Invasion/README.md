# Alien Invasion

Inspired by Space Invaders, Alien Invasion is an arcade game where the user has to use a ship to destroy all the aliens in the screen to 
reach the next level. As the levels increase, the aliens and the ship's bullets both move faster, the user has to steer the ship dexterously
to create a new high score. The game ends when either the aliens collide with the ship or they reach the bottom of the screen.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisities

Since this game is created using Pygame modules. You will need to install Pygame and its dependencies.

**On Linux:**
Install the dependencies first using the packet manager.
```
$ sudo apt-get install python3-dev mercurial
$ sudo apt-get install libsdl-image1.2-dev libsdl2-dev libsdl-ttf2.0-dev
```
If you want to add sounds to the game, install the following libraries as well:
```
$ sudo apt-get install libsdl-mixer1.2-dev libportmidi-dev
$ sudo apt-get install libswscale-dev libsmpeg-dev libavformat-dev libavcode-dev
$ sudo apt-get install python-numpy
```
Then finally install Pygame using pip:
```
$ pip install --user hg+http://bitbucket.org/pygame/pygame
```

**On OSX:**
Install the dependencies using [Homebrew](brew.sh).
```
$ brew install hg sdl sdl_image sdl_ttf
```
*see [Troubleshooting](#troubleshooting) for OSX's SDL bug*

And for sound libraries:
```
$ brew install sdl_mixer portmidi
```

Ending by installing Pygame using pip:
```
$ pip3 install --user hg+http://bitbucket.org/pygame/pygame
```

**On Windows**

Find a [windows installer](https://bitbucket.org/pygame/pygame/downloads/) that matches your version of Python.
Run the installer if it is an exe and if there is an .whl file copy it to the project directory.
Open a command window and navigate to the folder your copied your installer and install using pip.
```
> python -m pip install --user pygame-1.9.2a0-cp35-none-win32.whl
```

### Installing

No installation is needed! To play the game, run the *[alien_invasion.py](alien_invasion.py)* file using Python3 and enjoy!

### Controls

* Press the Return key(⏎) or click the 'Play' button to start
* Steer the ship using arrow keys(←↑↓→)
* Press 'q' to quit anytime.
* Press 'p' to pause the game.

##Troubleshooting

###1. Is this game compatible with Python 2.7 ?
    No, I am sorry, this game can only be run using Python3. 

###2. The game images aren't loading properly on my OSX. What do I do?
    This is the OSX's SDL image glitch I was talking about. You probably have a relatively newer version of SDL.
    This is what is making the images load incorrectly. You can solve this problem by degrading the SDL version down to 1.2.10. 
    There are several ways to do this, I found this method the best. Run this on your Terminal:
```
brew edit sdl_image
```
    This will open a ruby file. Update the URL and has as follows:
```
url "https://www.libsdl.org/projects/SDL_image/release/SDL_image-1.2.10.tar.gz"
sha256 "75e05d1e95f6277b44797157d9e25a908ba8d08a393216ffb019b0d74de11876"
```
    Comment out the newer version's URL and Hash for backup if you want. Now run:
```
brew reinstall sdl_image
```


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
