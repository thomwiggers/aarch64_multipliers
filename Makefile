#CXX=clang++

.PHONY: all
all: test measuremult

mult4.s: mult4.py library.py
	python $< > $@

mult8.s: mult8.py library.py
	python $< > $@

mult16.s: mult16.py library.py
	python $< > $@

%.o: %.s
	$(AS) -o $@ $<

%.o: %.cpp bit.hpp
	$(CXX) -Ofast -c -o $@ $<

test: test.cpp mult4.o mult8.o dmult4.o dmult8.o karatmult8.o karatmult16.o dmult16.o
	$(CXX) -O2 -o $@ $^

measuremult: measuremult.cpp cpucycles.cpp mult4.o dmult4.o dmult8.o mult8.o karatmult8.o dmult16.o karatmult16.o
	$(CXX) -Ofast -fomit-frame-pointer -o $@ $^
