CC = gcc
CFLAGS = -Wall -g

# Directories containing C code
C_DIR = Handout/Socket Coding Examples/C
RAW_DIR = Handout/Socket Coding Examples/C Raw Sockets

.PHONY: all clean c_examples raw_examples

all: c_examples raw_examples

c_examples:
	$(MAKE) -C "$(C_DIR)" all

raw_examples:
	$(MAKE) -C "$(RAW_DIR)" all

clean:
	$(MAKE) -C "$(C_DIR)" clean
	$(MAKE) -C "$(RAW_DIR)" clean
