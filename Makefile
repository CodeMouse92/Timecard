#!/usr/bin/make -f

clean:
	rm -rf dist/
	rm -rf build/
	rm -rf venv_make/

configure: clean
	python3 -m venv venv_make
	venv_make/bin/pip install pyinstaller
	venv_make/bin/pip install -r requirements.txt

build: configure
	venv_make/bin/pyinstaller --clean --windowed timecard_app.spec

build_folder: configure
	venv_make/bin/pyinstaller --clean --windowed timecard_app_folder.spec

.PHONY: clean configure build build_folder
