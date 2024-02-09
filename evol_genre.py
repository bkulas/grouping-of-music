#%%
import mgr
import music21
import numpy as np
import evolutionary.evol_func as ev
import random
import pygad
#%%
CHARACTERISTIC_NUMBER = 7
CATEGORIES = 2

#%%
poprock = []
softrock = []
#%%
with open(r'dataset/poprock.txt', 'r') as fp:
    for line in fp:
        x = line[:-1]
        poprock.append(x)
# %%
with open(r'dataset/softrock.txt', 'r') as fp:
    for line in fp:
        x = line[:-1]
        softrock.append(x)

# %%
poprock10 = poprock[:10]
softrock10 = softrock[:10]
melody_pr = [music21.converter.parse(i)for i in poprock10]
melody_sr = [music21.converter.parse(i)for i in softrock10]
# %%
motives_pr = [mgr.analyseComposition(i,0) for i in melody_pr]
motives_sr = [mgr.analyseComposition(i,0) for i in melody_sr]
# %%
small_motives_pr = [i[0] for i in motives_pr]
small_motives_sr = [i[0] for i in motives_sr]
#%%
space = [ev.flatten(small_motives_pr), ev.flatten(small_motives_sr)]
#%%

# Maximize difference of sums (sum of differences)
def fitness_func(ga_instance, solution, solution_idx):
    sol = ev.group_in_categories(solution, CATEGORIES, CHARACTERISTIC_NUMBER)
    # SUM_positives: sum of distances between solution and motives in "good" categories
    SUM_positives = 0
    for i in range(len(sol)):
        SUM_positives += ev.sum_for_solution(sol[i], space[i])
    # SUM_negatives: sum of distances between solution and motives in "bad" categories
    SUM_negatives = 0
    for i in range(len(sol)):
        for j in range(len(space)):
            if i != j:
                SUM_negatives += ev.sum_for_solution(sol[i], space[j])   
    # difference between the sums
    fitness = SUM_positives - SUM_negatives
    return fitness

def callback_generation(ga_instance):
    global last_fitness
    print(f"Generation = {ga_instance.generations_completed}")
    print(f"Fitness    = {ga_instance.best_solution()[1]}")
    print(f"Change     = {ga_instance.best_solution()[1] - last_fitness}")
    last_fitness = ga_instance.best_solution()[1]

# %%
fitness_function = fitness_func
#%%
num_generations = 100 # Number of generations.
num_parents_mating = 7

sol_per_pop = 50 # Number of solutions in the population.
num_genes = CHARACTERISTIC_NUMBER*CATEGORIES
initial_population = []
for i in range(sol_per_pop):
    s = []
    for j in range(CATEGORIES):
        s.append(random.sample(ev.flatten(space), CHARACTERISTIC_NUMBER))
    initial_population.append(ev.flatten(s))

last_fitness = 0
#%%
# Creating an instance of the GA class inside the ga module. Some parameters are initialized within the constructor.
ga_instance = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating, 
                       fitness_func=fitness_function,
                       #sol_per_pop=sol_per_pop, 
                       #num_genes=num_genes,
                       gene_space=space, #check redundancy
                       initial_population=initial_population,
                       mutation_type="random",
                       mutation_probability=0.2,
                       on_generation=ev.callback_generation)
#%%
# Running the GA to optimize the parameters of the function.
ga_instance.run()

# After the generations complete, some plots are showed that summarize the how the outputs/fitenss values evolve over generations.
ga_instance.plot_fitness()
# napisać funkcję celu z uwzględnieniem podobieństw motywów.

# #Podobieństwo dwóch motywów jako średnia podobieństw pomiędzy wszystkimi realizacjami
# # motive2, motive2: lista rzeczywistych realizacji
# def motives_similarity_matrix(motive1: list, motive2: list):
#     sim = []
#     for i in range(len(motive1)):
#         sim.append([])
#         for j in range(len(motive2)):
#             sim[i].append(0)   
#     for i in range(len(motive1)):
#         for j in range(len(motive2)):
#             print(i)
#             sim[i][j] = mgr.countSimilarity(motive1[i],motive2[j])
#     sums = [sum(i) for i in sim]
#     avg = sum(sums)/(len(sim)*len(sim[0]))
#     return sim, avg
# # %%
# # Podobieństwo utworów: uwaga na długości motywów
# # group1, group2: lista motywów złoonych z realizacji uporządkowanych wg długości
# # group_avr_sim - tablica średnich wartości podobieństw wszystkich realizacji motywów
# def group_similarity(group1: list, group2: list):
#     group_avr_sim = []
#     if len(group1) >= len(group2):
#         motives_count = len(group1)
#     else: motives_count = len(group2)
#     for l in range(motives_count):
#         avr = []
#         for i in range(len(group1[l])):
#             avr.append([])
#             for j in range(len(group2[l])):
#                 avr[i].append(0)
#         group_avr_sim.append(avr) 
#     for l in range(motives_count):
#         avr=[]
#         for i in range(len(group1[l])):
#             avr.append([])
#             for j in range(len(group2[l])):
#                 _ , a = motives_similarity_matrix(group1[l][i],group2[l][j])
#                 avr[i].append(a)
#         group_avr_sim[l] = avr
#     return group_avr_sim

# # %%
# # Funkcja do obliczania sumy maksymalnych wartości niemniejszych niz limit w wierszach lub kolumnach macierzy mat
# def max_and_sum_matrix(mat: list, limit = 0):
#     sum1 = 0
#     sum2 = 0
#     for i in mat:
#         if max(i) >= limit:
#             sum1 += max(i)
#     matT = np.array(mat).transpose()
#     for i in matT:
#         if max(i) >= limit:
#             sum2 += max(i)
#     if sum2 > sum1:
#         return  sum2
#     return sum1
# # %%
