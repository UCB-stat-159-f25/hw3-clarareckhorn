.PHONY : outputs
outputs : isles.dat abyss.dat sierra.dat last.dat

# Count words.

isles.dat : books/isles.txt
	python countwords.py $< $@

abyss.dat : books/abyss.txt
	python countwords.py $< $@

sierra.dat : books/sierra.txt
	python countwords.py $< $@

last.dat : books/last.txt
	python countwords.py $< $@

.PHONY : clean
clean : figures, audio, _build
	rm -f *.dat

.PHONY : env
clean : figures, audio, _build
	rm -f *.dat

.PHONY : html
clean : figures, audio, _build
	rm -f *.dat