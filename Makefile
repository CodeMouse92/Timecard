ROOT_DEST=/opt/timecard-app
ROOT_BIN=/usr/bin
ROOT_APPS=/usr/share/applications/
ROOT_ICONS=/usr/share/icons/hicolor/scalable/apps/

USER_DEST=/home/${USER}/.timecard-app
USER_BIN=/home/${USER}/.local/bin/
USER_APPS=/home/${USER}/.local/share/applications/
USER_ICONS=/home/${USER}/.icons/hicolor/scalable/apps/

DESKTOP_FILE=com.indeliblebluepen.timecard_app.desktop
ICON_FILE=timecard.svg

none:
	@echo "install			Install Timecard in a virtual environment."
	@echo "uninstall		Uninstall Timecard."

install:
ifeq "${USER}" "root"

ifneq ("$(wildcard $(ROOT_BIN)/timecard-app)","")
	$(error timecard-app already installed at ${ROOT_BIN})
endif

	@echo "Install as root..."
	sudo python3 -m venv --system-site-packages ${ROOT_DEST}
	sudo ${ROOT_DEST}/bin/python3 setup.py install
	sudo ln -s ${ROOT_DEST}/bin/timecard-app ${ROOT_BIN}/timecard-app

	sudo cp timecard/resources/${DESKTOP_FILE} ${ROOT_APPS}.
	sudo chmod +x ${ROOT_APPS}${DESKTOP_FILE}
	sudo cp timecard/resources/${ICON_FILE} ${ROOT_ICONS}.
	sudo update-icon-caches ${ROOT_ICONS}*
else

ifneq ("$(wildcard $(USER_BIN)/timecard-app)","")
	$(error timecard-app already installed at ${USER_BIN})
endif

	@echo "Installing as user..."
	python3 -m venv --system-site-packages ${USER_DEST}
	${USER_DEST}/bin/python3 setup.py install
	ln -s ${USER_DEST}/bin/timecard-app ${USER_BIN}/timecard-app

	cp timecard/resources/${DESKTOP_FILE} ${USER_APPS}.
	chmod +x ${USER_APPS}${DESKTOP_FILE}
	mkdir -p ${USER_ICONS}
	cp timecard/resources/${ICON_FILE} ${USER_ICONS}.
	update-icon-caches ${USER_ICONS}*
endif

uninstall:

ifeq "${USER}" "root"

ifeq ("$(wildcard $(ROOT_DEST))","")
	$(error timecard-app not installed at ${ROOT_DEST})
else
	@echo Uninstalling from ${ROOT_DEST}...
	rm -r ${ROOT_DEST}
	rm -rf ${ROOT_BIN}/timecard-app
	rm -rf ${ROOT_APPS}${DESKTOP_FILE}
	rm -rf ${ROOT_ICONS}${ICON_FILE}
endif

else

ifeq ("$(wildcard $(USER_DEST))","")
	$(error timecard-app not installed at ${USER_DEST})
else
	@echo Uninstalling from ${USER_DEST}...
	rm -r ${USER_DEST}
	rm -rf ${USER_BIN}/timecard-app
	rm -rf ${USER_APPS}${DESKTOP_FILE}
	rm -rf ${USER_ICONS}${ICON_FILE}
endif

endif

.PHONY: install uninstall test
