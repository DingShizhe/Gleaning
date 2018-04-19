SRC_LOC:= ./src/
DES_LOC:= ./
TEX:=xelatex
TEX_FLAG:=-quiet -synctex=1 -interaction=nonstopmode --clean

all: target

target:
	./gen.sh $(SRC_LOC) $(DES_LOC)
	xelatex  $(SRC_LOC)main.tex -o $(DES_LOC)main.pdf > /dev/null

clean:
	./clean.sh
