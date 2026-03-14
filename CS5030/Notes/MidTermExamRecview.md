# Mid Term Exam Review

## 1. Architectures & Performance

**Pipelining:** Break an instruction into stages (fetch, decode, execute…). While stage 1 processes instruction B, stage 2 processes instruction A. Startup/drain cost at beginning/end. Multiple issue = multiple instructions per cycle. Out-of-order execution fills pipeline bubbles with independent instructions.

**Cache:** Accessed in blocks (cache lines, 8–16 words). Row-major access → cache hits (spatial locality). Column access → cache misses (different memory blocks). Temporal locality = reusing recently accessed data. Spatial locality = accessing nearby data.

**Flynn's Taxonomy:**
| | Single Data | Multiple Data |
|---|---|---|
| **Single Instruction** | SISD (serial CPU) | SIMD (GPUs, vector) |
| **Multiple Instruction** | MISD (rare, fault-tolerant) | MIMD (multicore, clusters) |

**UMA** = all cores same memory access time. **NUMA** = cores faster to local memory.

**Performance:**

- **Speedup:** $$S = \frac{T_{serial}}{T_{parallel}}$$
- **Efficiency** (p = # processors, ideal = 1.0): $$E = \frac{S}{p}$$
- **Amdahl's Law** (even 90% parallel, max speedup → 10x): $$T_{parallel} = (1-f) \cdot T_{serial} + \frac{f \cdot T_{serial}}{p} \implies S = \frac{1}{(1-f) + \frac{f}{p}}$$
  - `f` = parallel fraction (0–1), `1-f` = serial fraction, `p` = # processors, `S` = speedup
- **Strong scaling:** fixed problem size, increase p → time decreases then flattens.
- **Weak scaling:** increase problem size proportional to p → time stays flat.

**Overhead:** $$T_{parallel} = \frac{T_{serial}}{p} + T_{overhead}$$ As p↑, overhead dominates.

---

## 2. Threads (Pthreads & C++11)

**Key idea:** Threads share heap/global memory. Each thread has its own stack. `my_rank` identifies each thread.

### Pthreads API
```c
#include <pthread.h>
pthread_t thread_handles[N];
// Create:  pthread_create(&thread_handles[i], NULL, func, (void*)i);
// Join:    pthread_join(thread_handles[i], NULL);
// Compile: gcc -g -Wall -o prog prog.c -lpthread
```
Thread function signature: `void* func(void* rank)` — cast rank back: `long my_rank = (long) rank;`

### C++11 Threads
```cpp
#include <thread>
std::thread t1(function_name);   // function pointer
std::thread t2(FunctionObject());// function object
std::thread t3([]{ /*...*/ });   // lambda
t1.join();
```

### Work Splitting Pattern (memorize this)
```c
int local_n = n / thread_count;
int my_first = my_rank * local_n;
int my_last  = my_first + local_n;  // exclusive end
for (i = my_first; i < my_last; i++) { /* work */ }
```

---

## 3. Race Conditions & Synchronization

**Race condition:** Multiple threads read/write shared variable simultaneously → incorrect results.
**Critical section:** Code that accesses shared resource — only one thread at a time.

### Busy-Waiting
```c
while (flag != my_rank);  // spin until my turn
sum += my_sum;
flag = (flag + 1) % thread_count;
```
Pros: enforces order. Cons: wastes CPU cycles, scales poorly (bad past ~16 threads).

### Mutex (Mutual Exclusion)
```c
pthread_mutex_t mutex;
pthread_mutex_init(&mutex, NULL);
pthread_mutex_lock(&mutex);
/* critical section */
pthread_mutex_unlock(&mutex);
pthread_mutex_destroy(&mutex);
```
Sleeps waiting thread (saves CPU). No guaranteed order. Better than busy-wait at scale.

### Semaphores
```c
#include <semaphore.h>
sem_t sem;
sem_init(&sem, 0, initial_val);
sem_wait(&sem);   // decrement; block if 0
sem_post(&sem);   // increment; unblock a waiter
sem_destroy(&sem);
```
More flexible than mutex — can allow up to N concurrent accesses.

### Read-Write Locks
```c
pthread_rwlock_t rwlock;
pthread_rwlock_rdlock(&rwlock);  // multiple readers OK
pthread_rwlock_wrlock(&rwlock);  // exclusive writer
pthread_rwlock_unlock(&rwlock);
```
Best when majority of operations are **reads (Member)**. Writers block all others.

### Barriers
All threads wait until everyone arrives, then proceed together. Used for: synchronizing phases, timing slowest thread, debugging.

### Condition Variables (C++)
```cpp
std::condition_variable cv;
cv.wait(lock, []{ return condition; });  // block until condition true
cv.notify_one();  // wake one waiter
```

**Deadlock:** Circular wait — Thread A holds lock 1, waits for lock 2; Thread B holds lock 2, waits for lock 1.

**Thread safety:** A function is thread-safe if multiple threads can call it simultaneously without errors. `strtok` is NOT thread-safe (static internal state). Use `strtok_r` instead.

---

## 4. OpenMP

```c
#include <omp.h>
// Compile: gcc -g -Wall -fopenmp -o prog prog.c
```

### Core Directives
```c
// Fork threads:
#pragma omp parallel num_threads(N)
{ /* parallel region — each thread runs this block */ }

// Parallel for (auto-splits iterations):
#pragma omp parallel for num_threads(N)
for (i = 0; i < n; i++) { /* ... */ }

// Critical section (like mutex):
#pragma omp critical
global_sum += local_sum;

// Reduction (compiler handles partial sums + combine):
#pragma omp parallel for reduction(+: sum)
for (i = 0; i < n; i++) sum += f(i);
```

### Variable Scope
| Scope | Meaning |
|-------|---------|
| **shared** (default) | All threads see same variable |
| **private** | Each thread gets its own uninitialized copy |
| **reduction(op: var)** | Private copies, combined with op at end |
| **default(none)** | Forces explicit declaration of every variable |

**Rule:** Variables defined *before* parallel region are shared by default. Variables defined *inside* are private. Loop index in `parallel for` is automatically private.

### Data Dependencies
If iteration i depends on iteration i−1, you CANNOT safely parallelize with `parallel for`. Fix: recompute the dependent value from the loop index (e.g., `factor = (k%2==0) ? 1.0 : -1.0` instead of `factor = -factor`).

### Pragma omp for vs parallel for
- `parallel for` = fork threads + split loop (combined).
- `for` inside an existing `parallel` region = split loop among already-forked team.
- Two `for` inside one `parallel` = same team does both loops.
- Two `parallel for` = two separate teams created/destroyed.

### Conditional Compilation
```c
#ifdef _OPENMP
  int tc = omp_get_num_threads();
#else
  int tc = 1;
#endif
```

### Key Functions
- `omp_get_thread_num()` → my rank
- `omp_get_num_threads()` → total threads in team

---

## 5. Quick-Reference Decision Table

| Problem | Solution |
|---------|----------|
| Shared variable updated by all threads | `reduction` clause or `critical` section |
| Need threads to finish phase before next | Barrier |
| Mostly read operations on shared data | Read-write lock |
| Enforce execution order | Busy-wait (or semaphores) |
| Variable changes each iteration | Make it `private` or recompute from index |
| Linked list with mixed read/write | Single mutex (simple) or rwlock (if read-heavy) |
