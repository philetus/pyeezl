pyeezl
======

python implementation of eezl, a simple interface for interactive vector graphics

dependencies
------------

* [numpy](http://www.numpy.org/) for vectors and matrices
* [pyopengl](http://pyopengl.sourceforge.net/) wrapper for [opengl](https://www.opengl.org/) graphics library
* [pyglfw](https://bitbucket.org/pyglfw/pyglfw) wrapper for [glfw](http://www.glfw.org/) for windowing, events and opengl context
* [pynanovg](https://github.com/philetus/pynanovg) wrapper for [nanovg](https://github.com/memononen/nanovg) for drawing 2d vector graphics to opengl context


installation
------------

install homebrew
follow instructions [here](http://brew.sh/)


install python3

    $ brew install python3


install gcc (for gfortran for numpy) (2hours)

    $ brew install gcc


install numpy, cython and pyopengl

    $ pip3 install numpy
    $ pip3 install cython
    $ pip3 install pyopengl


install glfw and python wrapper

    $ brew tap homebrew/versions
    $ brew install --build-bottle glfw3
    $ pip3 install pyglfw


build and install pynanovg

    $ brew install freetype
    $ git clone https://github.com/philetus/pynanovg
    $ cd pynanovg/nanovg
    $ git submodule init
    $ git submodule update
    $ cd ../
    $ python3 setup.py build 
    $ mkdir pynanovg
    $ cp -r build/lib.<system>/pynanovg ./


build and install pyeezl, test with example script

    $ git clone https://github.com/philetus/pyeezl (clone in same folder as pynanovg)
    $ cd pyeezl/examples
    $ ln -s ../pyeezl ./
    $ ln -s ../../pynanovg/pynanovg ./
    $ python3 rubber_bands.py
