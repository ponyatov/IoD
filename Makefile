MERGE  = README.md Makefile .gitignore
MERGE += requirements.txt IoD.py metacircular.py
MERGE += static templates
MERGE += upy
MERGE += droid
MERGE += doc
merge:
	git checkout master
	git checkout ponyatov -- $(MERGE)
