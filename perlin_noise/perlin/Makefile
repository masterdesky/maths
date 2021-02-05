CC				=		clang++ -std=c++17
OPTIMIZE	=		-O3 -Wall
IDIR			=		include
SDIR			=		src
CFLAGS		=		$(OPTIMIZE) -I$(IDIR)

ODIR			=		obj
LDIR			=		lib
LIBS			=		-lm

_DEPS			=		template.h generate_grid.h
DEPS			=		$(patsubst %,$(IDIR)/%,$(_DEPS))

_OBJ			=		generate_perlin_noise.o generate_grid.o 
OBJ				=		$(patsubst %,$(ODIR)/%,$(_OBJ))


$(ODIR)/%.o: $(SDIR)/%.cpp $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

perlin: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS) $(LIBS)

.PHONY: clean

clean:
	rm -f $(ODIR)/*.o *~ core $(IDIR)/*~