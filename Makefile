.PHONY: build
build: venv
	uv build


.PHONY: test
test: venv
	uv run tox


.PHONY: dist-clean
dist-clean: clean
	rm -rf .venv
	rm -rf src/vfbLib.egg-info


.PHONY: clean
clean:
	rm -rf build dist htmlcov .tox .coverage


.PHONY: update
update:
	rm -f uv.lock
	uv lock


.PHONY: venv
venv: .venv/.lock


.venv/.lock:
	uv sync --group test
