

#for finding ranges of yards 



def play_choice(down, ytd, time, distance):
    return (down * ytd * time)/ distance







down = 1
ytd = 1
time = 0

distance = 30

listy1 = []
listy2 = []
listy3 = []

for i in range(30, 70):
    for j in range(down, 4):
        for k in range(51, 60):
            for l in range(ytd, 10):
                listy1.append(play_choice(j, l, k, i))

for i in range(71, 90):
    for j in range(down, 4):
        for k in range(51, 60):
            for l in range(ytd, 10):
                listy2.append(play_choice(j, l, k, i))

for i in range(91, 100):
    for j in range(down, 4):
        for k in range(51, 60):
            for l in range(ytd, 10):
                listy3.append(play_choice(j, l, k, i))


print(min(listy1))
print(max(listy1))

print(min(listy2))
print(max(listy2))

print(min(listy3))
print(max(listy3))

