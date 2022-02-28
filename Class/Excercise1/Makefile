# Makefile 
CC = gcc
LFLAGS = 
CFLAGS =
SRC = src/
BIN = bin/



tests : $(SRC)test_de.c
	$(CC) -o $(BIN)main_test $(SRC)my_timing.c $(SRC)fish_production_single.c $(SRC)Linkedlist.c $(SRC)fish_production_stucs.c $(LFLAGS)
	./$(BIN)main_test


clean:
	rm $(BIN)main_test
