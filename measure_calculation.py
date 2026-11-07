import platform
import timeit

from quote import total_cents


def workload():
    for seats in range(1, 201):
        total_cents(1250, seats)


samples = timeit.repeat(workload, number=100, repeat=5)
print(platform.python_version())
print("Seconds for each 20000-call sample:")
for sample in samples:
    print(f"{sample:.6f}")
