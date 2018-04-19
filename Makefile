SRC_LOC:= ./src/
DES_LOC:= ./build/
TEX:=xelatex
TEX_FLAG:=-quiet -synctex=1 -interaction=nonstopmode --clean

all: target

target:
	./gen.sh $(SRC_LOC) $(DES_LOC)
	xelatex  $(SRC_LOC)main.tex -o -output-directory=$(DES_LOC) > /dev/null
	# xelatex  $(SRC_LOC)main.tex -o -output-directory=$(DES_LOC)

clean:
	./clean.sh
