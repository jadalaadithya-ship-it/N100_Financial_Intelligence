import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.analytics.cagr import calculate_cagr

print("Test 1:", calculate_cagr(100, 200, 5)[1] == "NORMAL")
print("Test 2:", calculate_cagr(100, -50, 5)[1] == "DECLINE_TO_LOSS")
print("Test 3:", calculate_cagr(-100, 200, 5)[1] == "TURNAROUND")
print("Test 4:", calculate_cagr(-100, -50, 5)[1] == "BOTH_NEGATIVE")
print("Test 5:", calculate_cagr(0, 100, 5)[1] == "ZERO_BASE")
print("Test 6:", calculate_cagr(100, 200, 5, 3)[1] == "INSUFFICIENT")
print("Test 7:", calculate_cagr(100, 200, 5)[0] is not None)
print("Test 8:", calculate_cagr(50, 100, 5)[0] > 0)
print("Test 9:", calculate_cagr(100, 150, 3)[1] == "NORMAL")
print("Test 10:", calculate_cagr(80, 160, 4)[1] == "NORMAL")