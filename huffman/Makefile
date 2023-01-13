# Assumes that util.py is correct/finished and in current working directory
# Assumes that directory structure is as provided
CASE=0

now:
	# Can change this
	make test

push:
	git commit -a
	git push

validate:
	@echo "No submission validator for Assn. 2"
	test -f not.a.file
	# python3 submission_validator.py

pep8:
# Might have to do, in the VM:  sudo apt install pep8
	pep8 util.py

check:
	python3 version.py
	ls -lt Expected
	ls -lt Tests
	ls -lt wwwroot

test:
	make decomp CASE=1 FILE=test.1.txt
	make decomp CASE=2 FILE=index.html
	make decomp CASE=3 FILE=favicon.ico
	make decomp CASE=4 FILE=arrow.png
	make decomp CASE=5 FILE=oval.png
	make decomp CASE=6 FILE=huffman.bmp
	make both CASE=7 FILE=Tests/x.test.1.txt
	make both CASE=8 FILE=Tests/x.arrow.png
	make both CASE=9 FILE=Tests/x.oval.png

prep:
	# NOT part of our actual testing, but part of preparations
	@echo "Only to be used by intructor..."
	test -f not.a.file
	make comp FILE=Expected/test.1.txt
	make comp FILE=Expected/arrow.png
	make comp FILE=Expected/oval.png
	mv Expected/test.1.txt.huf Tests
	mv Expected/arrow.png.huf Tests
	mv Expected/oval.png.huf Tests
	make comp FILE=Expected/favicon.ico
	make comp FILE=Expected/huffman.bmp
	make comp FILE=Expected/index.html
	cp Expected/favicon.ico.huf Tests
	cp Expected/huffman.bmp.huf Tests
	cp Expected/index.html.huf Tests
	mv Expected/favicon.ico.huf wwwroot
	mv Expected/huffman.bmp.huf wwwroot
	mv Expected/index.html.huf wwwroot
	make check

## Be careful of effects of image cache
server:
	(cd wwwroot; python3 ../webserver.py)

## Decompress only
decomp:
	@echo "***************************"
	@echo "** Test " $(CASE) ": Decompress --> " $(FILE)
	python3 decompress.py Tests/$(FILE).huf
	cmp Expected/$(FILE) Tests/$(FILE).huf.decomp
	cksum Expected/$(FILE) Tests/$(FILE).huf.decomp
	@echo "** Passed: " $(CASE) " Decompress --> " $(FILE)
	@echo "***************************"

## Compress only
comp:
	@echo "***************************"
	@echo "** Test: Compress --> " $(FILE)
	python3 compress.py $(FILE)
	@echo "** Done: Compress --> " $(FILE)
	@echo "***************************"

## Compress and Decompress
both:
	@echo "***************************"
	@echo "** Test " $(CASE) "Part (1): Compress --> " $(FILE)
	python3 compress.py $(FILE)
	@echo "** Test " $(CASE) "Part (2): Decompress --> " $(FILE)
	python3 decompress.py $(FILE).huf
	cmp $(FILE) $(FILE).huf.decomp
	cksum $(FILE) $(FILE).huf.decomp
	@echo "** Passed " $(CASE) ": Decompress --> " $(FILE)
	@echo "***************************"

clean:
	# For MacOS
	-rm .DS_Store
	-rm -r __pycache__
	-rm Tests/*decomp
	-rm Tests/x*huf
