# First create a file, with a couple of lines
with open('Tests/test.txt', 'w') as f:
    for i in range(1, 5):
        f.write(f'Number {i}\n')

# Now add some extra lines using append mode
with open('Tests/test.txt', 'a') as f:
    for i in range(5, 20):
        f.write(f'Append number {i}\n')
with open('Tests/test.txt') as f:
    print(f.read())