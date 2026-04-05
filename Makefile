.PHONY: all preprocess pdf epub site verify clean dev

all: preprocess pdf epub site verify

preprocess:
	python3 scripts/build.py --preprocess

pdf: preprocess
	python3 scripts/build.py --pdf

epub: preprocess
	python3 scripts/build.py --epub

site: preprocess
	python3 scripts/build.py --site

verify:
	python3 scripts/verify.py

clean:
	rm -rf build/

dev: site
	cd site && mint dev
