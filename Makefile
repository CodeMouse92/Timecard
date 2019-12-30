#!/usr/bin/make -f

none:
	@echo "build			Build as single file."
	@echo "build_folder		Build as single folder."
	@echo "clean			Clean build artifacts."

clean:
	rm -rf dist/
	rm -rf build/
	rm -rf venv_make/

configure: clean
	python3 -m venv venv_make
	venv_make/bin/pip install pyinstaller
	venv_make/bin/pip install -r requirements.txt

build: configure
	venv_make/bin/pyinstaller --clean --windowed timecard-app.spec

build_folder: configure
	venv_make/bin/pyinstaller --clean --windowed timecard-app_folder.spec

.PHONY: clean configure build build_folder
