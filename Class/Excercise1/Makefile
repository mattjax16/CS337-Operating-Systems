# Makefile 
CC = gcc
LFLAGS = 
CFLAGS =
SRC = src/
BIN = bin/



fish_production_single_mac : $(SRC)fish_production_single.c
	$(CC) -o $(BIN)fish_production_single $(SRC)my_timing.c $(SRC)fish_production_single.c $(SRC)Linkedlist.c $(SRC)fish_production_stucs.c $(LFLAGS)
	./$(BIN)fish_production_single


# Inference rules
%.o : %.c
	$(CC) $(CFLAGS)-c -o $@ $^
