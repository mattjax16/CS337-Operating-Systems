




CC = clang++

All: test_default_ctor
	./test_default_ctor


test_default_ctor: bigint.o test_default_ctor.cpp
	$(CC) bigint.o test_default_ctor.cpp -o test_default_ctor


bigint.o: bigint.cpp bigint.hpp
	$(CC) bigint.cpp -c

clean:
	rm *.o
	rm test_default_ctor test_c_str_ctor test_int_ctor
