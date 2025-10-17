import random

# ------------------------------
# Problem Setup
# ------------------------------
values = [60, 100, 120]       # values of items
weights = [10, 20, 30]        # weights of items
capacity = 50                 # maximum weight of knapsack

num_items = len(values)
num_nests = 10                # number of nests (population)
Pa = 0.25                     # discovery probability
MaxGen = 50                   # max generations


# ------------------------------
# Helper Functions
# ------------------------------
def random_solution():
    """Generate a random 0/1 solution (nest)."""
    return [random.randint(0, 1) for _ in range(num_items)]

def fitness(solution):
    """Compute fitness (total value), penalize if overweight."""
    total_weight = sum(weights[i] * solution[i] for i in range(num_items))
    total_value = sum(values[i] * solution[i] for i in range(num_items))
    if total_weight > capacity:
        return 0  # invalid solution (too heavy)
    return total_value

def levy_flight(solution):
    """Create new solution by flipping a few bits randomly."""
    new_sol = solution[:]
    i = random.randint(0, num_items - 1)
    new_sol[i] = 1 - new_sol[i]  # flip bit (0 -> 1 or 1 -> 0)
    return new_sol


# ------------------------------
# Initialize Nests
# ------------------------------
nests = [random_solution() for _ in range(num_nests)]
fitness_values = [fitness(sol) for sol in nests]


# ------------------------------
# Cuckoo Search Main Loop
# ------------------------------
for gen in range(MaxGen):
    for i in range(num_nests):
        # Generate a new solution using Levy flight
        new_sol = levy_flight(nests[i])
        new_fit = fitness(new_sol)

        # Choose a random nest to compare
        j = random.randint(0, num_nests - 1)
        if new_fit > fitness_values[j]:
            nests[j] = new_sol
            fitness_values[j] = new_fit

    # Abandon a fraction Pa of worst nests
    sorted_nests = sorted(zip(fitness_values, nests), reverse=True)
    num_abandon = int(Pa * num_nests)

    for k in range(num_abandon):
        new_random = random_solution()
        sorted_nests[-(k+1)] = (fitness(new_random), new_random)

    # Update nests and fitness values
    fitness_values, nests = zip(*sorted_nests)
    fitness_values, nests = list(fitness_values), list(nests)


# ------------------------------
# Best Solution
# ------------------------------
best_index = fitness_values.index(max(fitness_values))
best_solution = nests[best_index]
best_value = fitness_values[best_index]
best_weight = sum(weights[i] * best_solution[i] for i in range(num_items))

print("Best Solution (items selected):", best_solution)
print("Total Value:", best_value)
print("Total Weight:", best_weight)
