.PHONY: test setup clean run-checkpoints

setup:
	python scripts/setup_db.py

test: setup
	behave tests/features/ -v

run-checkpoints: setup
	python scripts/run_checkpoints.py

clean:
	rm -f data/banking.db
	rm -f reports/*.html

all: setup run-checkpoints test