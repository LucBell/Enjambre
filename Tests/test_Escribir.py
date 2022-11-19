with open('test.txt', 'w') as f:
    for i in range(1, 5):
        f.write(str(i))
with open('test.txt', 'r') as f:
    print(f.read())