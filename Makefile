doc:
	mkdir -p doc
html: doc
	epydoc -v --graph=all --html **/*.py *.py -o doc/html
pdf: doc
	epydoc -v --graph=all --pdf **/*.py *.py -o doc/pdf
latex: doc
	epydoc -v --graph=all --latex **/*.py *.py -o doc/latex
clean:
	rm -rf doc/pdf ; rm -rf doc/html ; rm -f **/*.pyc *.pyc **/*.pyo *.pyo ; rm -rf __pycache__ ; rm -rf main.dist
run:
	python src/main.py || python3 src/main.py
compile:
	python3 -m py_compile src/**/*.py *.py
exe_win:
	nuitka --standalone --recurse-all --remove-output --windows-icon=icon.ico main.py
	cp -r resource main.dist ; cp config.txt main.dist
exe_mac: exe
exe_lin: exe
exe:
	nuitka --standalone --recurse-all --remove-output --clang --lto main.py
	cp -r resource main.dist ; cp config.txt main.dist
pip:
	pip3 install -r requirements.txt

