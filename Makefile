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
	nuitka3 --follow-imports --standalone --remove-output --windows-icon=icon.ico src/main.py
	cp -r resource main.dist ; cp config.txt main.dist
exe_mac: exe
exe_lin: exe
exe:
	nuitka3 --follow-imports --standalone --remove-output --clang src/main.py
	cp -r resource main.dist ; cp config.txt main.dist
dep:
	pip3 install -r requirements.txt
	sudo apt install -y nuitka pydoctor

