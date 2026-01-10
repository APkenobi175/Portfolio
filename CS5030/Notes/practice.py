def balance_interations(n, p):
    n= 15 # number of iterations
    p= 3 # number of cores
    # Total time on each core
    time = [0]*p # This will create a list of p zeros.

    print ("Initial time:", time)

    iterations = [] # compile a list of iterations for each core. (list of lists)
    for i in range(p):
        iterations.append([])
    print ("Initial iterations:", iterations)

    # Now that we have our data structures, we can start assigning iterations to cores.

    for i in range(n, 0, -1): # start from n downt o 1
        # find core with minimum time
        min_core = time.index(min(time))

        # assign iteration i to that core
        iterations[min_core].append(i)
        time[min_core] += i # update total time for that core (add i)
        print("Final time:", time)
        print("Iterations assigned to each core:", iterations)


balance_interations(15, 3)
