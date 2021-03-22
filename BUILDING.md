# Building

Timecard can be built and run a number of ways.

## setup.py

You can build Timecard directly using its `setup.py` file. We recommend
doing so in a virtual environment:

```bash
python3 setup.py install
```

If you're on a Linux system, you can also install from the `setup.py` and
automatically create and place the `.desktop` and icon files using the
provided Makefile. Run as user for a local install, or as `sudo` for a
(safe) system-wide installation.

```bash
make install
```

## Building with PyInstaller

To build Timecard, we recommend using Python 3.7 and creating a virtual
environment.

Run the following in a virtual environment to build Timecard:

```bash
pip install pyinstaller
pip install -r requirements.txt
pyinstaller --clean --windowed timecard-app.spec
```

The distribution folder is `dist/timecard-app`, and the standalone binary is
at `dist/timecard-app/timecard-app`.

