nums = input().split()
list = ""
while len(nums) >= 11 or len(nums) < 0:
    nums = input().split()
for num in nums:
    if num not in list:
        list += num + " "

print(list)
