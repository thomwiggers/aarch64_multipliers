#CXX=clang++

.PHONY: all
all: test measuremult

.DELETE_ON_ERRROR: mult32.s mult16.s mult8.s mult4.s

mult4.s: mult4.py
	python $< > $@

mult8.s: mult8.py mult4.py
	python $< > $@

mult16.s: mult16.py mult8.py mult4.py
	python $< > $@

mult32.s: mult32.py mult16.py mult8.py mult4.py
	python $< > $@

mult33.s: mult33.py mult32.py mult16.py mult8.py mult4.py
	python $< > $@

mult64.s: mult64.py mult32.py mult16.py mult8.py mult4.py
	python $< > $@

%.o: %.s
	$(AS) -o $@ $<

%.o: %.cpp bit.hpp
	$(CXX) -Ofast -mtune=cortex-a53 -c -o $@ $<

test: test.cpp mult4.o mult8.o dmult4.o dmult8.o karatmult8.o karatmult16.o dmult16.o mult16.o dmult32.o karatmult32.o cmult32.o mult32.o dmult33.o cmult33.o mult33.o mult64.o dmult64.o karatmult64.o cmult64.o
	$(CXX) -o $@ $^

measuremult: measuremult.cpp cpucycles.cpp mult4.o dmult4.o dmult8.o mult8.o karatmult8.o dmult16.o karatmult16.o mult16.o dmult32.o karatmult32.o cmult32.o mult32.o dmult33.o mult33.o cmult33.o mult64.o dmult64.o karatmult64.o cmult64.o
	$(CXX) -Ofast -mtune=cortex-a53 -fomit-frame-pointer -o $@ $^
