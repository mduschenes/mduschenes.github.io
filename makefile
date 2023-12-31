SHELL := /bin/bash
ECHO := echo
CP := cp -rf
MKDIR := mkdir -p
MV := mv -f
EXE := bundle
OPTIONS := exec jekyll server

PORT := 4000
FLAGS := --port $(PORT) &
RESET := $(shell lsof -n -i | grep $(EXE) | awk '{ print $$2 }' | tr "\n" " " | sort -V | xargs kill -9)

DIRECTORY := .
SOURCE := _config.yml index.md
DESTINATION :=
CONFIG := $(patsubst %,$(DIRECTORY)/%,$(CONFIG))

DIRECTORY := /home/${USER}/files/documents/resume/resume
SOURCE := resume.pdf resume.bib
DESTINATION := assets/data/
FILES := $(patsubst %,$(DIRECTORY)/%,$(SOURCE))

all : setup
	@$(EXE) $(OPTIONS) $(FLAGS)

setup :
	@$(CP) $(FILES) $(DESTINATION)

clean :
	@$(RESET)

.PHONY : all clean setup
.SILENT : all clean setup