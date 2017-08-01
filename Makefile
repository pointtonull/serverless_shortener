SRC = $(PWD)/src
REQUIREMENTS = $(SRC)/requirements.txt
AWS_PROFILE = tudev
PYTHON = python
CHALICE = chalice --project-dir $(SRC)
STAGE = dev

.PHONY: unit test coverage deploy clean delete

deps: .deps
.deps: $(REQUIREMENTS) requirements.txt
	pip install -r requirements.txt
	pip install -r $(REQUIREMENTS)
	touch .deps

deploy: deps
	$(CHALICE) deploy --profile $(AWS_PROFILE) --no-autogen-policy --stage $(STAGE)

delete: deps
	$(CHALICE) delete --profile $(AWS_PROFILE) --stage $(STAGE)

clean:
	@echo "Cleaning all artifacts..."
	@-rm -rf _build
	@-rm .deps

run: deps
	$(CHALICE) local

unit test: deps $(TOOLS)
	cd $(SRC);\
	$(PYTHON) -m pytest ../tests

coverage: deps $(TOOLS)
	cd $(SRC);\
	$(PYTHON) -m pytest ../tests --cov $(SRC) --cov-report=term-missing ../tests
