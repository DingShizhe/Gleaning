TEX:=xelatex
TEX_FLAG:=-quiet -synctex=1 -interaction=nonstopmode --clean

all: target

target:
	if test -d build; then rm build -rf; fi
	mkdir build && cp src/* build -r;
	cd build && python3 build.py;
	# xelatex main.tex -o -output-directory=$(DES_LOC) > /dev/null
	# xelatex main.tex -o -output-directory=$(DES_LOC) > /dev/null
	xelatex main.tex -o -output-directory=..
clean:
	if test -d build; then rm build -rf; fi
	rm main* *log
