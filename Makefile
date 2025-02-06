
bundle.toycsp:
bundle.%:
	cd $* && python bundler.py > ../build/$*_bundle.py && cd ..