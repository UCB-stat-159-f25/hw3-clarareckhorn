ENV_NAME = ligo-analysis1
PYTHON = python
MYS = myst

.PHONY: env html clean help

env:
	@if conda env list | grep -q "^$(ENV_NAME) "; then \
		conda env update -n $(ENV_NAME) -f environment.yml; \
	else \
		conda env create -f environment.yml; \
	fi

# build the myst site
html:
	myst build --html

# Clean to delete the generated files
clean:
	rm -rf figures/*
	rm -rf audio/*
	rm -rf _build/*