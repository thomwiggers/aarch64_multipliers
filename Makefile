
.PHONY: all
all: test measuremult

mult4.s: mult4.py
	python $< > $@

mult8.s: mult8.py
	python $< > $@

%.o: %.s
	$(AS) -o $@ $<

test: test.cpp bit.hpp mult4.o mult8.o dmult4.cpp dmult8.cpp karatmult8.cpp
	$(CXX) -O2 -o $@ $^

measuremult: measuremult.cpp cpucycles.cpp mult4.o dmult4.cpp
	$(CXX) -Ofast -fomit-frame-pointer -o $@ $^
