
APP_NAME_LOWER=timecard-app
APP_NAME_UPPER=Timecard-App

ROOT_DEST=/opt/${APP_NAME_LOWER}
ROOT_BIN=/usr/bin
ROOT_APPS=/usr/share/applications/
ROOT_ICONS=/usr/share/icons/hicolor/scalable/apps/

USER_DEST=/home/${USER}/.${APP_NAME_LOWER}
USER_BIN=/home/${USER}/.local/bin/
USER_APPS=/home/${USER}/.local/share/applications/
USER_ICONS=/home/${USER}/.icons/hicolor/scalable/apps/

SHARE_PATH=share
DESKTOP_FILE_PATH=${SHARE_PATH}/applications
DESKTOP_FILE=com.codemouse92.timecard.desktop
ICON_FILE_PATH=${SHARE_PATH}/icons
ICON_FILE=com.codemouse92.timecard.svg

none:
	@echo "install			Install Timecard in a virtual environment."
	@echo "uninstall		Uninstall Timecard."

install:
ifeq "${USER}" "root"

ifneq ("$(wildcard $(ROOT_BIN)/${APP_NAME_LOWER})","")
	$(error ${APP_NAME_LOWER} already installed at ${ROOT_BIN})
endif

	@echo "Install as root..."
	sudo python3 -m venv --system-site-packages ${ROOT_DEST}
	sudo ${ROOT_DEST}/bin/python3 setup.py install
	sudo ln -s ${ROOT_DEST}/bin/${APP_NAME_UPPER} ${ROOT_BIN}/${APP_NAME_LOWER}
	sudo ln -s ${ROOT_DEST}/bin/${APP_NAME_UPPER} ${ROOT_BIN}/${APP_NAME_UPPER}

	sudo cp ${DESKTOP_FILE_PATH}/${DESKTOP_FILE} ${ROOT_APPS}.
	sudo chmod +x ${ROOT_APPS}${DESKTOP_FILE}
	sudo cp ${ICON_FILE_PATH}/${ICON_FILE} ${ROOT_ICONS}.

	# note: update-icon-caches may not exist on certain distros
	-sudo update-icon-caches ${ROOT_ICONS}*
else

ifneq ("$(wildcard $(USER_BIN)/${APP_NAME_LOWER})","")
	$(error ${APP_NAME_LOWER} already installed at ${USER_BIN})
endif

	@echo "Installing as user..."
	python3 -m venv --system-site-packages ${USER_DEST}
	${USER_DEST}/bin/python3 setup.py install
	mkdir -p ${USER_BIN}
	ln -s ${USER_DEST}/bin/${APP_NAME_UPPER} ${USER_BIN}/${APP_NAME_LOWER}
	ln -s ${USER_DEST}/bin/${APP_NAME_UPPER} ${USER_BIN}/${APP_NAME_UPPER}

	cp ${DESKTOP_FILE_PATH}/${DESKTOP_FILE} ${USER_APPS}.
	chmod +x ${USER_APPS}${DESKTOP_FILE}
	mkdir -p ${USER_ICONS}
	cp ${ICON_FILE_PATH}/${ICON_FILE} ${USER_ICONS}.

	# note: update-icon-caches may not exist on certain distros
	-update-icon-caches ${USER_ICONS}*
endif

uninstall:

ifeq "${USER}" "root"

ifeq ("$(wildcard $(ROOT_DEST))","")
	$(error ${APP_NAME_LOWER} not installed at ${ROOT_DEST})
else
	@echo Uninstalling from ${ROOT_DEST}...
	rm -r ${ROOT_DEST}
	rm -rf ${ROOT_BIN}/${APP_NAME_LOWER}
	rm -rf ${ROOT_BIN}/${APP_NAME_UPPER}
	rm -rf ${ROOT_APPS}${DESKTOP_FILE}
	rm -rf ${ROOT_ICONS}${ICON_FILE}
endif

else

ifeq ("$(wildcard $(USER_DEST))","")
	$(error ${APP_NAME_LOWER} not installed at ${USER_DEST})
else
	@echo Uninstalling from ${USER_DEST}...
	rm -r ${USER_DEST}
	rm -rf ${USER_BIN}/${APP_NAME_LOWER}
	rm -rf ${USER_BIN}/${APP_NAME_UPPER}
	rm -rf ${USER_APPS}${DESKTOP_FILE}
	rm -rf ${USER_ICONS}${ICON_FILE}
endif

endif

.PHONY: install uninstall test
