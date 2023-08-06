import time
from . import _shunting_yard as shunt

expressions = [
	"3 + ((4 + 3 / 2) / 3.284)"
]

start = time.time()
expr = shunt._infix_to_postfix(expressions[0])
for i in range(100000):
	shunt._eval_postfix(expr)
end = time.time()

print(f"My eval took: {end-start} seconds") 

start = time.time()
for i in range(100000):
	eval(expressions[0])
end = time.time()

print(f"Python eval took: {end-start} seconds") 
