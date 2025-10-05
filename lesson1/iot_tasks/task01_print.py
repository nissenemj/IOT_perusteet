# Tulosta numerot 0–9 ja aikaleiman
import time
time.sleep(0.1)
nums = list(range(10))
for n in nums:
    print("[%s] %d" % (time.ticks_ms(), n))
print("Summa:", sum(nums))
