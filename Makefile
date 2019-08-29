MERGE  = Makefile .gitignore
MERGE += requirements.txt IoD.py metacircular.py
MERGE += static templates
merge:
	git checkout master
	git checkout ponyatov -- $(MERGE)