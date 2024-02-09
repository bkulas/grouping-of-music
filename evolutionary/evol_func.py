# @author: Barbara Laskowska
# FUnkcje algorytmu ewolucyjnego opartego o struktury motywów muzycznych
import mgr
import numpy as np

def flatten(input):
    list = []
    for row in input:
        list.extend(row)
    return list

#Podobieństwo dwóch motywów jako średnia podobieństw pomiędzy wszystkimi realizacjami
# motive2, motive2: lista rzeczywistych realizacji
def motives_similarity_matrix(motive1: list, motive2: list):
    sim = []
    for i in range(len(motive1)):
        sim.append([])
        for j in range(len(motive2)):
            sim[i].append(0)   
    for i in range(len(motive1)):
        for j in range(len(motive2)):
            print(i)
            sim[i][j] = mgr.countSimilarity(motive1[i],motive2[j])
    sums = [sum(i) for i in sim]
    avg = sum(sums)/(len(sim)*len(sim[0]))
    return sim, avg

# Podobieństwo utworów: uwaga na długości motywów
# group1, group2: lista motywów złoonych z realizacji uporządkowanych wg długości
# group_avr_sim - tablica średnich wartości podobieństw wszystkich realizacji motywów
def group_similarity(group1: list, group2: list):
    group_avr_sim = []
    if len(group1) >= len(group2):
        motives_count = len(group1)
    else: motives_count = len(group2)
    for l in range(motives_count):
        avr = []
        for i in range(len(group1[l])):
            avr.append([])
            for j in range(len(group2[l])):
                avr[i].append(0)
        group_avr_sim.append(avr) 
    for l in range(motives_count):
        avr=[]
        for i in range(len(group1[l])):
            avr.append([])
            for j in range(len(group2[l])):
                _ , a = motives_similarity_matrix(group1[l][i],group2[l][j])
                avr[i].append(a)
        group_avr_sim[l] = avr
    return group_avr_sim

# Funkcja do obliczania sumy maksymalnych wartości niemniejszych niz limit w wierszach lub kolumnach macierzy mat
def max_and_sum_matrix(mat: list, limit = 0):
    sum1 = 0
    sum2 = 0
    for i in mat:
        if max(i) >= limit:
            sum1 += max(i)
    matT = np.array(mat).transpose()
    for i in matT:
        if max(i) >= limit:
            sum2 += max(i)
    if sum2 > sum1:
        return  sum2
    return sum1

def sum_of_sets(first_list, second_list):
    set1 = set(first_list)
    set2 = set(second_list)
    return (set1 & set2)

def sum_for_simple_solution(selected, motives_cat):
    sum = 0
    for i in range(len(motives_cat)):
        sum += len(sum_of_sets(selected, motives_cat[i]))
    return sum

def sum_for_solution(selected, motives_cat):
    sum = 0
    for i in range(len(motives_cat)):
        sum += max_and_sum_matrix(group_similarity(selected, motives_cat[i]))
    return sum

def group_in_categories(solution, categories, number_of_char):
    sol = []
    for i in range(categories):
        for j in range(number_of_char):
            if j == 0:
                sol.append([solution[i*number_of_char+j]])
            else:
                sol[i].append(solution[i*number_of_char+j])
    return sol

