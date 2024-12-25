SHELL := /bin/bash
ECHO := echo
CP := cp -rf
MKDIR := mkdir -p
MV := mv -f
CONVERT := pdftk
PING := ping
GET := wget -r --auth-no-challenge --convert-links --retry-connrefused
SLEEP := sleep 3
EXE := bundle
OPTIONS := exec jekyll server -l

NAME := ~/Downloads/website
HOST := localhost
PORT := 4000
FLAGS := --host $(HOST) --port $(PORT) &
RESET := lsof -n -i | grep $(EXE) | awk '{ print $$2 }' | tr "\n" " " | sort -V | xargs --no-run-if-empty kill  -9

DIRECTORY := .
SOURCE := _config.yml index.md
DESTINATION :=
CONFIG := $(patsubst %,$(DIRECTORY)/%,$(CONFIG))

DIRECTORY := /home/${USER}/files/documents/resume
SOURCE := resume/resume.pdf bib/bib.pdf
DESTINATION := assets/data/resume/cv.pdf
FILES := $(patsubst %,$(DIRECTORY)/%,$(SOURCE))

all : setup clean
	@$(EXE) $(OPTIONS) $(FLAGS)

setup :
	@$(CONVERT) $(FILES) cat output $(DESTINATION)

static : all
	@$(GET) $(HOST):$(PORT)
	@$(MV) $(HOST):$(PORT) $(NAME)

clean :
	-@$(RESET)
	-@$(RM) $(NAME)

.PHONY : all clean setup static
.SILENT : all clean setup static