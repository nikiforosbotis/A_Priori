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


def GetAllUniqueItems(name):   #η μέθοδος αυτή κάθε φορά που καλείται επιστρέφει όλα τα μοναδικά στοιχεία του αρχείου.
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

def GetUniqueItems(basket):   #η μέθοδος αυτή είναι όπως η ζητούμενη στην περιγραφή του αλγορίθμου. Πέρνει ως όρισμα ένα καλάθι και επιστρέφει ένα set που περιέχει τα μοναδικά στοιχεία του καλαθιού.
    unique = set(basket)
    return unique

def GetPairs(s):   #η μέθοδος GetPairs(s) δέχεται ως όρισμα ένα λεξικό και επιστρέφει μια λίστα η οποία περιέχει όλα τα πιθανά ζεύγη.
    pairs = itertools.combinations(s, 2)
    pairs_list = []
    for pair in pairs:
        pairs_list.append(pair)
    return pairs_list

def A_Priori_Algorithm_First_Pass(file, s):   #εδώ γίνεται το πρώτο πέρασμα του αλγορίθμου, όπου το αποτέλεσμα είναι ένα λεξικό με τις συχνότητες των μοναδικών στοιχείων κάθε καλαθιού.

    input_file = open(file, 'r')
    csv_reader = csv.reader(input_file, delimiter=',')

    if(args.numeric == True):   #αν το αρχείο input έχει αριθμούς, αυτή η συνθήκη επιτρέπει να τους χειριστεί αναλόγως.
        
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
    
    while(i < len(baskets)):   #για κάθε διαφορετικό καλάθι, ακολουθείται η εξής διαδικασία.
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
    if(args.percentage == True):   #αν ο αριθμός που δίνει ο χρήστης μέσω του support αντιστοιχεί σε ποσοστό (σύμφωνα με την εκφώνηση) τότε το πρόγραμμα μπαίνει σε αυτό το βρόχο.
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

def A_Priori_Algorithm_Next_Passes(file, freqk, k, s):   #η μέθοδος αυτή είναι ουσιαστικά η κύρια υλοποίηση του αλγορίθμου, που περιέχει τα επόμενα (μετά το 1ο) περάσματα.

    input_file = open(file, 'r')
    csv_reader = csv.reader(input_file, delimiter=',')

    
    if(args.numeric == True):   #αντίστοιχα με την προηγούμενη μέθοδο, αφορά την περίπτωση που το αρχείο csv περιέχει αριθμούς.
        
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

    while(i < len(baskets)):   #για κάθε διαφορετικό καλάθι βρίσκουμε τα μοναδικά του στοιχεια και κατόπιν τα ζευγάρια και τις συχνότητες αυτών.
        items = GetUniqueItems(baskets[i])
        items_list = list(items)
        itemset_pairs = GetPairs(freqk)
        u = 0
        candidates = []
        q = 0
        while(q < len(itemset_pairs)):   #για κάθε ξεχωριστο ζευγάρι ακολουθείται η παρακάτω διαδικασια.
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
                            
                        if(args.percentage == True):   #αν το support που δίνει ο χρήστης αντιστοιχεί σε ποσοστό, τοτε το πρόγραμμα εισάγεται σε αυτό τον βρόγχο.
                            if(counts[tuple(final_list)] >= ((int(s)/100) * (len(baskets)))):   
                                if(tuple(final_list) in freq):
                                    del freq[tuple(final_list)]
                                freq[tuple(final_list)] = counts[tuple(final_list)]
                        else:
                            if(counts[tuple(final_list)] >= int(s)):
                                if(tuple(final_list) in freq):   #αν η λίστα (το tuple της) υπάρχει ήδη στο λεξικό, τότε την διαγράφουμε για να μπεί το νέο (αυξημένο) counts.
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

def A_Priori_Algorithm(file, s):   #ο κυρίος αλγόριθμος (ο οποίος καλέι τις προηγούμενες μεθόδους) φαίνεται σε αυτό το σημείο.
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

    return all_freq, results   #επιστρέφει τόσο το λεξικό (όπως λέει η εκφώνηση) όσο και την λίστα που περιέχει τα λεξικά ώστε να μας βοηθήσει στην εμφάνιση.

final_result, results = A_Priori_Algorithm(args.filename, args.support)   

if(isinstance(args.output, str) == True):   #αν ο χρήστης θέλει το πρόγραμμά του να αποθηκευτεί σε αρχείο.
    output_file = open(args.output, 'w')
    csv_writer = csv.writer(output_file, delimiter = ',')

    for row in list(final_result):
        csv_writer.writerow(row)

    output_file.close()
    
csv_writer = csv.writer(sys.stdout, delimiter=';')   #η εμφάνιση των αποτελεσμάτων στην οθόνη.

for freqs in results:
    row = []
    for key in sorted(freqs.keys()):
        row.append("{0}:{1}".format(key, freqs[key]))
    csv_writer.writerow(row)






