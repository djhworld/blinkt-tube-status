TARGET_DIR=./target
PACKAGE_NAME=blinkt-tube-status_1.0.0-1

all: clean prepare

clean:
	sudo rm -rf ${TARGET_DIR}

prepare:
	mkdir -p ${TARGET_DIR}/${PACKAGE_NAME}

package: all
	cp -a packaging/* ${TARGET_DIR}/${PACKAGE_NAME}/
	cp tube-status.py ${TARGET_DIR}/${PACKAGE_NAME}/usr/local/bin/blinkt-tube-status
	chmod +x ${TARGET_DIR}/${PACKAGE_NAME}/usr/local/bin/blinkt-tube-status
	cd ${TARGET_DIR} && find . | grep placeholder | xargs -I {} rm -v {}
	cd ${TARGET_DIR} && sudo chown -R root:root ./${PACKAGE_NAME} && dpkg-deb --build ${PACKAGE_NAME}



