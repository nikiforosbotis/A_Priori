import sys
import csv
import itertools
import argparse

parser = argparse
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--numeric", help="items are numeric",
                    action="store_true", default=False)
parser.add_argument("support", help="support threshold")
parser.add_argument("-p", "--percentage",
                    action="store_true", default=False,
                    help="treat support threshold as percentage value")
parser.add_argument("filename", help="input filename")
parser.add_argument("-o", "--output", type=str, help="output file")

args = parser.parse_args()

#Each time this method is called, it returns all the uniqe file's itmes.
def GetAllUniqueItems(name):
    with open(name, 'r') as f:
        result = set.union(*({field.strip().lower() for field in row}
                             for row in csv.reader(f, delimiter=',', skipinitialspace=True)))
    list_num = []
    if(args.numeric == True):
        for i in list(result):
            list_num.append(int(i))
    else:
        for i in list(result):
            list_num.append(i)

    return list_num

def GetUniqueItems(basket):
    unique = set(basket)
    return unique

#This methods takes a dictionary as an argument and returns a list with all the potential pairs.
def GetPairs(s):
    pairs = itertools.combinations(s, 2)
    pairs_list = []
    for pair in pairs:
        pairs_list.append(pair)
    return pairs_list

#The algorithm's first passage. It returns a dictionary containing the frequencies of the unique items of each basket.
def A_Priori_Algorithm_First_Pass(file, s):
    input_file = open(file, 'r')
    csv_reader = csv.reader(input_file, delimiter=',')
    #If the file contains numbers, these are manipulated accordingly.
    if(args.numeric == True):
        baskets_strings = []
        all_items = GetAllUniqueItems(file)
        for row in csv_reader:
            unique_row_items = set([field.strip().lower() for field in row])
            baskets_strings.append(unique_row_items)
        i = 0
        baskets = []
        while(i < len(baskets_strings)):
            basket = []
            for j in baskets_strings[i]:
                basket.append(int(j))
            baskets.append(basket)
            i = i + 1
    else:
        baskets = []
        all_items = GetAllUniqueItems(file)
        for row in csv_reader:
            unique_row_items = set([field.strip().lower() for field in row])
            baskets.append(unique_row_items)

    input_file.close()
    counts = {}
    freq = {}
    i = 0
    while(i < len(baskets)):
        items = GetUniqueItems(baskets[i])
        items_list = list(items)
        k = 0
        while(k < len(items_list)):
            if((items_list[k], ) not in counts):
                counts[(items_list[k], )] = 1
            else:
                counts[(items_list[k], )] = counts[(items_list[k], )] + 1
            k = k + 1
        i = i + 1
    i = 0
    if(args.percentage == True):
        while(i < len(all_items)):
            if(counts[(all_items[i], )] >= ((int(s)/100) * (len(baskets)))):
                freq[(all_items[i], )] = counts[(all_items[i], )]
            i = i + 1
    else:
        while(i < len(all_items)):
            if(counts[(all_items[i], )] >= int(s)):
                freq[(all_items[i], )] = counts[(all_items[i], )]
            i = i + 1
    return freq

#The main algorithm's implementation. It contains the passages >1.
def A_Priori_Algorithm_Next_Passes(file, freqk, k, s):
    input_file = open(file, 'r')
    csv_reader = csv.reader(input_file, delimiter=',')

    if(args.numeric == True):
        baskets_strings = []
        all_items = GetAllUniqueItems(file)
        for row in csv_reader:
            unique_row_items = set([field.strip().lower() for field in row])
            baskets_strings.append(unique_row_items)
        i = 0
        baskets = []
        while(i < len(baskets_strings)):
            basket = []
            for j in baskets_strings[i]:
                basket.append(int(j))
            baskets.append(basket)
            i = i + 1
    else:
        baskets = []
        all_items = GetAllUniqueItems(file)

        for row in csv_reader:
            unique_row_items = set([field.strip().lower() for field in row])
            baskets.append(unique_row_items)

    input_file.close()
    counts = {}
    freq = {}
    i = 0

    #For every single basket, we are finding the unique items and then the pairs and their sequencies.
    while(i < len(baskets)):
        items = GetUniqueItems(baskets[i])
        items_list = list(items)
        itemset_pairs = GetPairs(freqk)
        u = 0
        candidates = []
        q = 0
        while(q < len(itemset_pairs)):
            a1 = itemset_pairs[q][0]
            a2 = itemset_pairs[q][1]
            list_1 = []
            list_2 = []
            list_1.append(a1)
            list_2.append(a2)
            candidate = set(list_1).union(set(list_2))
            if(candidate not in candidates):
                candidates.append(candidate)
                candidate_list = list(candidate)

                if(k == 1):
                    candidate_list_completed = []
                    candidate_list_completed.append(candidate_list[0][0])
                    candidate_list_completed.append(candidate_list[1][0])
                    clc_set = set(candidate_list_completed)
                    final_list = list(clc_set)
                    if((len(final_list) == (k + 1)) and ((set(final_list) < items) or (set(final_list) == items))):
                        if(tuple(final_list) not in counts):
                            counts[tuple(final_list)] = 1
                        else:
                            counts[tuple(final_list)] = counts[tuple(final_list)] + 1
                        #if the support which is given as a percentage from the user, then this code is executed.
                        if(args.percentage == True):
                            if(counts[tuple(final_list)] >= ((int(s)/100) * (len(baskets)))):
                                if(tuple(final_list) in freq):
                                    del freq[tuple(final_list)]
                                freq[tuple(final_list)] = counts[tuple(final_list)]
                        else:
                            if(counts[tuple(final_list)] >= int(s)):
                                if(tuple(final_list) in freq):
                                    del freq[tuple(final_list)]
                                freq[tuple(final_list)] = counts[tuple(final_list)]
                elif(k == 2):
                    candidate_list_completed = []
                    candidate_list_completed.append(candidate_list[0][0])
                    candidate_list_completed.append(candidate_list[0][1])
                    candidate_list_completed.append(candidate_list[1][0])
                    candidate_list_completed.append(candidate_list[1][1])
                    clc_set = set(candidate_list_completed)
                    final_list = list(clc_set)
                    if((len(final_list) == (k + 1)) and ((set(final_list) in items) or (set(final_list) == items))):
                        if(tuple(final_list) not in counts):
                            counts[tuple(final_list)] = 1
                        else:
                            counts[tuple(final_list)] = counts[tuple(final_list)] + 1

                        if(args.percentage == True):
                            if(counts[tuple(final_list)] >= ((int(s)/100) * (len(baskets)))):
                                if(tuple(final_list) in freq):
                                    del freq[tuple(final_list)]
                                freq[tuple(final_list)] = counts[tuple(final_list)]
                        else:
                            if(counts[tuple(final_list)] >= int(s)):
                                if(tuple(final_list) in freq):
                                    del freq[tuple(final_list)]
                                freq[tuple(final_list)] = counts[tuple(final_list)] - 1
            q = q + 1
        i = i + 1

    return freq

def A_Priori_Algorithm(file, s):
    all_freq = {}
    results = []
    k = 1
    freqk = A_Priori_Algorithm_First_Pass(file, s)

    while(len(freqk) > 0):
        all_freq.update(freqk)
        results.append(freqk)
        freq = A_Priori_Algorithm_Next_Passes(file, freqk, k, s)
        freqk = freq
        k = k + 1

    return all_freq, results

final_result, results = A_Priori_Algorithm(args.filename, args.support)

#If the user wants the results to be saved in a file, this code segment is executed.
if(isinstance(args.output, str) == True):
    output_file = open(args.output, 'w')
    csv_writer = csv.writer(output_file, delimiter = ',')

    for row in list(final_result):
        csv_writer.writerow(row)

    output_file.close()

csv_writer = csv.writer(sys.stdout, delimiter=';')

for freqs in results:
    row = []
    for key in sorted(freqs.keys()):
        row.append("{0}:{1}".format(key, freqs[key]))
    csv_writer.writerow(row)
