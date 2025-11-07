import random

# ---------- Problem Setup ----------
tasks = [5, 8, 3, 7, 2, 6, 4, 9]   # time for each task
machines = 3                       # number of machines
grid_size = 10                     # number of cells (solutions)
iterations = 50                    # number of updates

# ---------- Helper Functions ----------
def makespan(schedule):
    """Calculate total time (load) on each machine, return max load."""
    loads = [sum(tasks[t] for t in m) for m in schedule]
    return max(loads)

def random_schedule():
    """Randomly assign tasks to machines."""
    sched = [[] for _ in range(machines)]
    for t in range(len(tasks)):
        m = random.randint(0, machines - 1)
        sched[m].append(t)
    return sched

def mutate(schedule):
    """Move one random task to a random machine."""
    new = [list(m) for m in schedule]
    src = random.choice([i for i in range(machines) if new[i]])  # pick non-empty
    task = random.choice(new[src])
    new[src].remove(task)
    dst = random.randint(0, machines - 1)
    new[dst].append(task)
    return new

# ---------- Initialize Population ----------
population = [random_schedule() for _ in range(grid_size)]
fitness = [makespan(s) for s in population]

# ---------- PCA Loop ----------
for it in range(iterations):
    new_population = []
    for i in range(grid_size):
        # pick 3 random neighbors
        neighbors = random.sample(range(grid_size), 3)
        best = min(neighbors, key=lambda j: fitness[j])
        # copy best and mutate
        child = mutate(population[best])
        new_population.append(child)
    # update
    population = new_population
    fitness = [makespan(s) for s in population]

# ---------- Output Best Solution ----------
best_index = fitness.index(min(fitness))
best_schedule = population[best_index]

print("\nBest makespan:", fitness[best_index])
for i, m in enumerate(best_schedule):
    load = sum(tasks[t] for t in m)
    print(f"Machine {i+1}: tasks {m}, load = {load}")
