s = 1e16 # this is a very large number
for i in range(1000000):
    s += 1e-9 # this is a tiny number
print(s) # this will print 1e16, because the tiny number is too small
            # to affect the large number due to roundoff error