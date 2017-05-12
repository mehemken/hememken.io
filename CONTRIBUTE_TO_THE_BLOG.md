# Contributing

To get started you'll need the [Anaconda distribution][2] of Python. Use Python 3.

You will also need to use `conda` to create the dependencies for this project.

    $ conda env create -f environment.yml

Then you'll need to use the command line tool to build the static site. The command line tool `command.py` allows you to do that easily.

    $ ./command.py -b

This command builds the static site in a sibling directory. So I recommend you have this directory structure:

    container-dir/
    ├── mehemken.io/
    └── build/

I have not tested this on any system but mine, so if you have trouble getting started, just let me know.

The posts live in `mehemken.io/pages/posts`

[1]: http://mehemken.io "The best website on the planet."
[2]: https://www.continuum.io/downloads
