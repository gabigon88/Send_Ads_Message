fileName = "user_id.txt"

unique = set()
fp = open(fileName, 'r') 
for uid in fp:
    unique.add(uid)
fp.close()

fp = open(fileName, 'w') 
for uid in unique:
    fp.write(uid)
fp.close()

print('complete')