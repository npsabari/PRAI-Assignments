f1 = open('docs.txt')
f2 = open('truth.txt')
a1 = []
a2 = []
for line in f1:
    words = line.strip().split()
    a1.append(words[0])
for line in f2:
    words = line.strip().split()
    a2.append(words[0])
for i in range(len(a1)):
    if a1[i] <> a2[i]:
        print 'cup'
print 'fine'
f1.close()
f2.close()
