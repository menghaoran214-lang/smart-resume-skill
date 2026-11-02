# Smart Resume - README generation and checks.
#
# README.md, README.zh-TW.md and README.en.md are products generated from
# templates/ and data/project.json. Edit the source, not the output.

PYTHON ?= python

.PHONY: help generate check test package

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

generate: ## Regenerate the three README files
	$(PYTHON) scripts/render_readme.py

check: ## Fail when a README is out of date
	$(PYTHON) scripts/render_readme.py --check

test: ## Run repository and skill tests
	$(PYTHON) -m unittest discover -s tests -v
	$(PYTHON) -m unittest discover -s skills/smart-resume/tests -v

package: ## Build the installable skill archive
	$(PYTHON) skills/smart-resume/scripts/package.py --out dist/smart-resume-skill-0.1.0.zip
