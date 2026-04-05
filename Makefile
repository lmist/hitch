.PHONY: all preprocess pdf epub site verify clean dev add

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

add:
	@test -n "$(URL)" || (echo "usage: make add URL=https://..." && exit 1)
	bun scripts/add-source.ts $(URL) $(AUTHOR)
