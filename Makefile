TEX:=xelatex
TEX_FLAG:=-quiet -synctex=1 -interaction=nonstopmode --clean

all: target

target:
	if test -d build; then rm build -rf; fi
	mkdir build && cp src/* build -r;
	cd build && python3 build.py;
	cd build && xelatex main.tex > /dev/null && xelatex main.tex > /dev/null;
	# cd build && xelatex main.tex && xelatexq main.tex > /dev/null;
	cp build/main.pdf main.pdf
clean:
	if test -d build; then rm build -rf; fi
	if test -f main.pdf; then rm main.pdf -rf; fi
