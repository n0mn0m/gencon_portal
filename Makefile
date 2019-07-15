SHELL := /bin/bash

copy: build save
	cp code.py /Volumes/PYPORTAL
	cp artifacts/menu.mpy /Volumes/PYPORTAL/lib
	cp artifacts/utils.mpy /Volumes/PYPORTAL/lib

save:
	mv lib/menu.mpy artifacts/
	mv lib/utils.mpy artifacts/

build:
	@pushd circuitpython/mpy-cross/ ; \
		./mpy-cross ../../lib/menu.py; \
		./mpy-cross ../../lib/utils.py; \
	popd

# https://learn.adafruit.com/building-circuitpython/build-circuitpython
get-mpy-cross:
	pip install huffman
	git clone https://github.com/adafruit/circuitpython.git;
	pushd circuitpython; \
	git submodule update --init --recursive; \
	popd
	pushd circuitpython/mpy-cross; \
	make; \
	popd
