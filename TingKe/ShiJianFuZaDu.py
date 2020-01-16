import time

start_time = time.time()
# for i in range(1,1001):
#     for j in range(1,1001):
#         for k in range(1,10001):
#             if i + k +j == 1000 and i**2 + j ** 2 == k **2:
#                 print(f"i:{i},j:{j},k:{k}")
for i in range(1,1001):
    for j in range(1,1001):
        k = 1000 - i - j
        if  i**2 + j ** 2 == k **2:
            print(f"i:{i},j:{j},k:{k}")

print(time.time()- start_time)
print("finished")