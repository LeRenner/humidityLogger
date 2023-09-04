board="esp32:esp32:esp32doit-devkit-v1"
boardDir="esp32.esp32.esp32doit-devkit-v1"
boardPort="/dev/ttyUSB0"

upload:
	rm -rf ./build/*
	arduino-cli compile --fqbn ${board} --export-binaries .
	sudo chmod 777 ${boardPort}
	arduino-cli upload --fqbn ${board} --input-dir ./build/${boardDir} -p ${boardPort}