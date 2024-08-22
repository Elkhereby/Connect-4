from Board import *
from Solver import *
import matplotlib.pyplot as plt

max_depth = 8
board = Board()
time_minmax = []
time_alpha_beta = []
time_expectiminimax = []
for i in range(max_depth+1):
    solver = Solver(depth=i)

    st = time.time()
    col_1, value = solver.solve(board)
    # print(col_1)
    end = time.time()
    t = float(end - st)
    time_alpha_beta.append(t)
    solver.algorithm = "minmax"
    st = time.time()
    col, value = solver.solve(board)
    # print(col_1)
    end = time.time()
    t = float(end - st)
    time_minmax.append(t)

    solver.algorithm = "ExpectMiniMax"
    st = time.time()
    col, value = solver.solve(board)
    # print(col_1)
    end = time.time()
    t = float(end - st)
    time_expectiminimax.append(t)



plt.plot(time_minmax,color='r',label="MinMax")


plt.plot(time_alpha_beta,color='b',label="α-β Pruning")
plt.plot(time_expectiminimax,color='cyan',label="ExpectMiniMax")
plt.legend()
plt.xlabel("Depth")
plt.ylabel("Time in seconds")
plt.savefig("Time Analysis.png")
plt.show()