ECHO := echo
CP := cp -rf
MKDIR := mkdir -p
MV := mv -f
EXE := bundle exec jekyll server
KILL := kill -9

PORT := 4000
FLAGS := --port $(PORT)

CONFIG := _config.yml index.md
FILES := 

SOURCE := .

FILES := $(patsubst %,$(SOURCE)/%,$(FILES))

SERVE : $(FILES)
	@$(ECHO) $(shell lsof -wni tcp:$(PORT) | grep TCP | tail | awk '{print $2}' )
	@$(EXE) $(FLAGS) &

$(FILES) :

$(SRC) :


.PHONY :
.SILENT :
