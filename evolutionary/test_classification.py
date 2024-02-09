#import evol_main as ev
from sklearn.metrics import classification_report, confusion_matrix

#dataset = ev.motives

# labels = []
# for i in ev.CATEGORIES:
#     labels.append([])
#     for j in ev.MELODIES_FOR_CATEGORY:
#         labels[i*ev.MELODIES_FOR_CATEGORY].append(i)

# X = ev.flatten(dataset)
# Y = ev.flatten(labels)

# characteristic = []
# for i in range(CATEGORIES):
#     for j in range(2):
#         print(i,j)
#         if j == 0:
#                 characteristic.append([solution[i*2+j]])
#         else:
#                 characteristic[i].append(solution[i*2+j])

def flatten(input):
    list = []
    for row in input:
        list.extend(row)
    return list
#%%
#function_inputs = [4,-2,3.5,5,-11,-4.7] # Function inputs.
#desired_output = 44 # Function output.

#%%
def sum_of_sets(first_list, second_list):
    set1 = set(first_list)
    set2 = set(second_list)
    return (set1 & set2)

#Classify motives from one piece
                #solution has sets of selected motives for every category
def classify(motives, solution):
    class_idx = 0
    max_sum = 0
    for i in range(len(solution)):
        sum = sum_of_sets(motives, solution[i])
        if len(sum) > max_sum:
            max_sum = len(sum)
            class_idx = i
    return (class_idx, max_sum)
        
def test_solution(motives_list, labels, solution):
    pred = []
    motives = flatten(motives_list)
    y_test = flatten(labels)
    for i in motives:
        cl , sum = classify(i,solution)
        pred.append(cl)
    print(confusion_matrix(y_test, pred))
    print(classification_report(y_test, pred))