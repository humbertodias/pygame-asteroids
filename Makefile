doc:
	mkdir -p doc
html: doc
	epydoc -v --graph=all --html **/*.py *.py -o doc/html
pdf: doc
	epydoc -v --graph=all --pdf **/*.py *.py -o doc/pdf
latex: doc
	epydoc -v --graph=all --latex **/*.py *.py -o doc/latex
clean:
	rm -rf doc/pdf ; rm -rf doc/html ; rm -f **/*.pyc *.pyc **/*.pyo *.pyo ; rm -rf __pycache__
run:
	python3 main.py || python3 main.py
compile:
	python3 -m py_compile **/*.py *.py
exe:
	nuitka --standalone --recurse-all --remove-output --windows-icon=resource/image/icon.png main.py
