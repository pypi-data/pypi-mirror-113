#!/usr/bin/python
# -*- coding: UTF-8 -*-

for i in range(1,5):
    for j in range(1,5):
        for k in range(1,5):
            if( i != k ) and (i != j) and (j != k):
                print(i, j, k)
f1 = 1
f2 = 1
for i in range(1,22):
    print('%12ld %12ld' % (f1, f2), end=' ')
    if (i % 3) == 0:
        print('')
    f1 = f1 + f2
    f2 = f1 + f2


if __name__ == '__main__':
    i = 0
    j = 1
    x = 0
    while (i < 5) :
        x = 4 * j
        for i in range(0,5) :
            if(x%4 != 0) :
                break
            else :
                i += 1
            x = (x/4) * 5 +1
        j += 1
    print (x)