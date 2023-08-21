# Recipe that uploads code to the Arduino board

board="arduino:avr:leonardo"
boardPath="arduino.avr.leonardo"
boardPort="/dev/ttyACM0"

upload:
	rm -rf ./build/*
	arduino-cli compile --fqbn ${board} --export-binaries .
	sudo chmod 777 ${boardPort}
	arduino-cli upload --fqbn ${board} --input-dir ./build/${boardPath} -p ${boardPort}
