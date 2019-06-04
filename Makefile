all: 
	cd src; $(MAKE); cd ..;
	rm -rf bin
	mkdir bin
	cp src/client bin/etgClient
	cp src/server bin/etgServer

clean: 
	cd src; $(MAKE) clean; cd ..;
	rm -rf bin

