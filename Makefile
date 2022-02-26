pep8:
	autopep8 -r -a -a -i ./

# Section: Deploy
test-deploy: build
	-pip install twine
	twine upload -r pypitest dist/*
test-install: requirements.txt
	pip install -r $<
	pip install --index-url https://test.pypi.org/simple/ graphform


install:
	./setup.py install
uninstall:
	-pip uninstall -y graphform
build: $(wildcard genice2/*.py genice2/formats/*.py genice2/lattices/*.py genice2/molecules/*.py)
	./setup.py sdist # bdist_wheel


deploy: build
	twine upload dist/*
check:
	./setup.py check

# Section: maintainance

clean:
	-rm -rf build dist
distclean:
	-rm *.scad *.yap @*
	-rm -rf build dist
	-rm -rf *.egg-info
	-rm .DS_Store
	find . -name __pycache__ | xargs rm -rf
	find . -name \*.pyc      | xargs rm -rf
	find . -name \*~         | xargs rm -rf
