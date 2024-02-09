# %%
import pygad
import random
import test_classification

#%% global
CHARACTERISTIC_NUMBER = 7
CATEGORIES = 2
MELODIES_FOR_CATEGORY = 50

#%%
# Create data set consists of characteristic motives from compositions
motives_first_cat = []
for i in range(MELODIES_FOR_CATEGORY):
    motives_first_cat.append(random.sample(range(0,50),5))
motives_second_cat = []
for i in range(MELODIES_FOR_CATEGORY):
    motives_second_cat.append(random.sample(range(20,60),5))
# motives_3_cat = []
# for i in range(MELODIES_FOR_CATEGORY):
#     motives_3_cat.append(random.sample(range(40,80),5))
# motives_4_cat = []
# for i in range(MELODIES_FOR_CATEGORY):
#     motives_4_cat.append(random.sample(range(60,100),5))
# motives_5_cat = []
# for i in range(MELODIES_FOR_CATEGORY):
#     motives_5_cat.append(random.sample(range(80,120),5))
motives = [motives_first_cat, motives_second_cat]#, motives_3_cat, motives_4_cat, motives_5_cat]
# Create data set depends on global parameter

#%% flatten sets of motives
def flatten(input):
    list = []
    for row in input:
        list.extend(row)
    return list
#%%
# Select solution as set of randomly choose sets of motives
all_motives = flatten([flatten(motives_first_cat), flatten(motives_second_cat)])

#%%
def sum_of_sets(first_list, second_list):
    set1 = set(first_list)
    set2 = set(second_list)
    return (set1 & set2)
#%%
def sum_for_solution(selected, motives_cat):
    sum = 0
    for i in range(len(motives_cat)):
        sum += len(sum_of_sets(selected, motives_cat[i]))
    return sum
#solution is a matrix 2 X 2 (number of categories x selected values)

#%%
def group_in_categories(solution, categories, number_of_char):
    sol = []
    for i in range(categories):
        for j in range(number_of_char):
            if j == 0:
                sol.append([solution[i*number_of_char+j]])
            else:
                sol[i].append(solution[i*number_of_char+j])
    return sol

# Maximize difference o sums (sum of differences)
def fitness_func(ga_instance, solution, solution_idx):
    sol = group_in_categories(solution, CATEGORIES, CHARACTERISTIC_NUMBER)
    # SUM_positives: sum of distances between solution and motives in "good" categories
    SUM_positives = 0
    for i in range(len(sol)):
        SUM_positives += sum_for_solution(sol[i], motives[i])
    # SUM_negatives: sum of distances between solution and motives in "bad" categories
    SUM_negatives = 0
    for i in range(len(sol)):
        for j in range(len(motives)):
            if i != j:
                SUM_negatives += sum_for_solution(sol[i], motives[j])   
    # difference between the sums
    fitness = SUM_positives - SUM_negatives
    return fitness
# Maximize minimum value of difference
def fitness_func_min(ga_instance, solution, solution_idx):
    sol = group_in_categories(solution, CATEGORIES, CHARACTERISTIC_NUMBER)
    positives = []
    diff = []
    for i in range(len(sol)):
        for j in range(len(motives[i])):
            if j == 0:
                positives.append([])
            positives[i].append(len(sum_of_sets(sol[i], motives[i][j])))
    negatives = []
    for i in range(len(sol)):
        for j in range(len(motives)):
            if j == 0:
                negatives.append([])
            if i != j:
                for k in range(len(motives[j])):
                    negatives[i].append(len(sum_of_sets(sol[i], motives[j][k])))
    for i in range(len(positives)):
            diff.append(sum(positives[i]) - sum(negatives[i]))
    avg = sum(diff)/len(diff)
    minimum = min(diff)
    return minimum
#%%
fitness_function = fitness_func
#%%
num_generations = 100 # Number of generations.
num_parents_mating = 7


# To prepare the initial population, there are 2 ways:
# 1) Prepare it yourself and pass it to the initial_population parameter. This way is useful when the user wants to start the genetic algorithm with a custom initial population.
# 2) Assign valid integer values to the sol_per_pop and num_genes parameters. If the initial_population parameter exists, then the sol_per_pop and num_genes parameters are useless.
sol_per_pop = 50 # Number of solutions in the population.
num_genes = CHARACTERISTIC_NUMBER*CATEGORIES
initial_population = []
for i in range(sol_per_pop):
    s = []
    for j in range(CATEGORIES):
        s.append(random.sample(all_motives, CHARACTERISTIC_NUMBER))
    initial_population.append(flatten(s))

last_fitness = 0
def callback_generation(ga_instance):
    global last_fitness
    print(f"Generation = {ga_instance.generations_completed}")
    print(f"Fitness    = {ga_instance.best_solution()[1]}")
    print(f"Change     = {ga_instance.best_solution()[1] - last_fitness}")
    last_fitness = ga_instance.best_solution()[1]

# Creating an instance of the GA class inside the ga module. Some parameters are initialized within the constructor.
ga_instance = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating, 
                       fitness_func=fitness_function,
                       #sol_per_pop=sol_per_pop, 
                       #num_genes=num_genes,
                       gene_space=all_motives, #check redundancy
                       initial_population=initial_population,
                       mutation_type="random",
                       mutation_probability=0.2,
                       on_generation=callback_generation)

# Running the GA to optimize the parameters of the function.
ga_instance.run()

# After the generations complete, some plots are showed that summarize the how the outputs/fitenss values evolve over generations.
ga_instance.plot_fitness()

# Returning the details of the best solution.
solution, solution_fitness, solution_idx = ga_instance.best_solution()
print(f"Parameters of the best solution : {solution}")
print(f"Fitness value of the best solution = {solution_fitness}")
print(f"Index of the best solution : {solution_idx}")


labels = []
for i in range(CATEGORIES):
    labels.append([])
    for j in range(MELODIES_FOR_CATEGORY):
        labels[i].append(i)

sol=group_in_categories(solution, CATEGORIES, CHARACTERISTIC_NUMBER)
test_classification.test_solution(motives,labels,sol)

""" #%%
prediction = numpy.sum(numpy.array(function_inputs)*solution)
print(f"Predicted output based on the best solution : {prediction}") """
# #% %
# if ga_instance.best_solution_generation != -1:
#     print(f"Best fitness value reached after {ga_instance.best_solution_generation} generations.")
# #%%
# # Saving the GA instance.
# filename = 'genetic' # The filename to which the instance is saved. The name is without extension.
# ga_instance.save(filename=filename)
# #%%
# # Loading the saved GA instance.
# loaded_ga_instance = pygad.load(filename=filename)
# loaded_ga_instance.plot_fitness()
# %%
