CXX := g++
CXXFLAGS := -std=c++23 -Wall -pedantic
TARGET := cholesky

SRCS := main.cpp matrix.cpp io.cpp cholesky.cpp
OBJS := $(SRCS:.cpp=.o)
HEADERS := matrix.hpp io.hpp cholesky.hpp misc.hpp

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) $(FLOAT_T_FLAG) -o $@ $(OBJS)

%.o: %.cpp $(HEADERS)
	$(CXX) $(CXXFLAGS) $(FLOAT_T_FLAG) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)

rebuild: clean $(TARGET)

.PHONY: clean rebuild

main.o: matrix.hpp io.hpp cholesky.hpp misc.hpp
matrix.o: matrix.hpp misc.hpp
io.o: io.hpp matrix.hpp misc.hpp
cholesky.o: cholesky.hpp matrix.hpp misc.hpp
