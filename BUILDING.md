# Building

To build Timecard, we recommend using Python 3.7 and creating a virtual
environment.

If you're on a Linux system, you can use the provided Makefile:

```
make build
```

Alternatively, run the following in a virtual environment to build Timecard:

```
pip install pyinstaller
pip install -r requirements.txt
pyinstaller --clean --windowed timecard-app.spec
```

The distribution folder is `dist/timecard-app`, and the standalone binary is
at `dist/timecard-app/timecard-app`.

## Debian Package

The Debian packaging is configured to build an executable using
a virtual environment and PyInstaller. Standard Debian packaging commands
apply.

WARNING: This should be considered experimental right now. I have yet to add
the rest of the dependencies stripped out of the PyInstaller.
