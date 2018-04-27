SRC_LOC:= ./src/
DES_LOC:= ./build/
TEX:=xelatex
TEX_FLAG:=-quiet -synctex=1 -interaction=nonstopmode --clean

all: target

target:
	./gen.sh $(SRC_LOC) $(DES_LOC)
	xelatex main.tex -o -output-directory=$(DES_LOC) > /dev/null

clean:
	./clean.sh
