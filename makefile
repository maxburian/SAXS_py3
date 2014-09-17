docu::
	cd doc&& $(MAKE)  html

pdf::
	cd doc && $(MAKE) latexpdf
	cp doc/_build/latex/SAXS.pdf .
