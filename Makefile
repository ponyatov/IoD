MERGE  = Makefile .gitignore
MERGE += requirements.txt IoD.py metacircular.py
merge:
	git checkout master
	git checkout ponyatov -- $(MERGE)