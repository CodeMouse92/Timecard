# Building

To build Timecard, we recommend using Python 3.7 and creating a virtual
environment.

Run the following in a virtual environment to build Timecard:

```
pip install pyinstaller
pip install -r requirements.txt
pyinstaller --clean --windowed timecard_app.spec
```

The distribution folder is `dist/timecard_app`. To start the application,
run `dist/timecard_app/timecard_app`.

## Debian Package

The Debian packaging is configured to build an executable using
a virtual environment and PyInstaller. Standard Debian packaging commands
apply.
