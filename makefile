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

DIRECTORY := /home/matt/files/documents/resume/resume
SOURCE := resume.pdf
DESTINATION := assets/data/cv.pdf
FILES := $(patsubst %,$(DIRECTORY)/%,$(SOURCE))

all : $(CONFIG) $(FILES)
	@$(ECHO) $(FILES) $(DESTINATION)
	@$(RESET)
	@$(EXE) $(OPTIONS) $(FLAGS)

$(FILES) :
	@$(CP) $(FILES) $(DESTINATION)

.PHONY : all
.SILENT : all