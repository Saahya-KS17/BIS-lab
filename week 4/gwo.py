import random

# ----------------------------
# Problem Setup (Tasks)
# ----------------------------
tasks = [3, 5, 2, 7, 4]   # Task durations (in hours)
num_tasks = len(tasks)
num_wolves = 6             # population size
max_iter = 50              # number of iterations

# ----------------------------
# Fitness Function
# ----------------------------
def fitness(schedule):
    """Lower total time = better fitness (negative for maximization form)."""
    total_time = sum(schedule)
    return -total_time

# ----------------------------
# Create Random Schedule (Wolf)
# ----------------------------
def random_schedule():
    s = tasks[:]
    random.shuffle(s)
    return s

# ----------------------------
# Initialize Wolves
# ----------------------------
wolves = [random_schedule() for _ in range(num_wolves)]
fitness_values = [fitness(w) for w in wolves]

# Identify alpha, beta, delta (top 3 wolves)
def update_leaders():
    sorted_indices = sorted(range(num_wolves), key=lambda i: fitness_values[i], reverse=True)
    return sorted_indices[0], sorted_indices[1], sorted_indices[2]

alpha, beta, delta = update_leaders()

# ----------------------------
# GWO Main Loop
# ----------------------------
for t in range(max_iter):
    a = 2 - 2 * (t / max_iter)  # control parameter decreasing from 2 to 0

    for i in range(num_wolves):
        X = wolves[i][:]  # current wolf

        # Generate new position guided by alpha, beta, delta
        for ref in [wolves[alpha], wolves[beta], wolves[delta]]:
            A = 2 * a * random.random() - a
            C = 2 * random.random()
            # position update simulated by partial swapping
            if abs(A) < 1:  # exploitation (follow best wolves)
                idx = random.randint(0, num_tasks - 1)
                X[idx] = ref[idx]

        # Shuffle slightly to maintain diversity
        random.shuffle(X)
        new_fit = fitness(X)

        if new_fit > fitness_values[i]:
            wolves[i] = X
            fitness_values[i] = new_fit

    # Update alpha, beta, delta
    alpha, beta, delta = update_leaders()

# ----------------------------
# Output Best Solution
# ----------------------------
best_schedule = wolves[alpha]
best_time = -fitness_values[alpha]

print("Best Task Schedule (order of durations):", best_schedule)
print("Total Completion Time:", best_time)
