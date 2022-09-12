"""
file: lab2.py
description: Checking if the provided clauses can be resoluted
language: python3
"""
import sys
from sys import argv
from itertools import combinations


Predicates = []
variables = []
constants = []
functions = []
clauses = []

def checknegation(s1, s2, index1, index2):
    """
        checking if one predicate is negation while other not
        if both negation, c_sum will be 2
        if none negation, c_sum will be 4
        if one negation and one non negation c_sum is 3
        :param s1: clause1
        :param s2: clause2
        :param index1: index at which predicate starts for s1
        :param index2: index at which predicate starts for s2
        :return: boolean value
        """
    c_sum = 0
    if (s1[index1 - 1] == '!'):
        c_sum += 1
    else:
        c_sum += 2

    # checking for second param
    if (s2[index2 - 1] == '!'):
        c_sum += 1
    else:
        c_sum += 2

    if c_sum == 3:
        return True
    else:
        return False


def argumentcheck(s1, s2, index1, index2):
    """
        checking if no. of values inside predicates are same
        :param s1: clause1
        :param s2: clause2
        :param index1: index at which predicate starts for s1
        :param index2: index at which predicate starts for s1
        :return: boolean and list of argument inside both clauses
        """
    start_index1 = s1[index1:].find('(') + index1 + 1
    end_index1 = s1[index1:].find(')') + index1
    start_index2 = s2[index2:].find('(') + index2 + 1
    end_index2 = s2[index2:].find(')') + index2
    list1 = s1[start_index1:end_index1].split(',')  # list to have all the variables inside predicate

    list2 = s2[start_index2:end_index2].split(',')
    if len(list1) == len(list2):
        return True, list1, list2
    else:
        return False, [], []


def resolute(s1, s2, pred):
    """
        negate two clauses and add remaining back to clause_list
        :param s1: clause1
        :param s2: clause2
        :param pred: the common predicate in both clauses
        :return:
        """
    global clauses

    clause1_list = s1.split()
    for val in clause1_list:
        if val.find(pred) >= 0:
            clause1_list.remove(val)
    # if len(clause1_list) > 0:


    # clause list 2:
    clause2_list = s2.split()
    for val in clause2_list:
        if val.find(pred) >= 0:
            clause2_list.remove(val)

    result_str = " ".join(clause1_list + clause2_list)

    if len(result_str) == 0:
        return True,[s1,s2],[result_str]
    else:
        return False,[s1,s2],[result_str]



def unificationcheck(s1, s2, pred):
    predicate_index1 = s1.find(pred)
    predicate_index2 = s2.find(pred)

    # check if both clausees have same number of arguments

    if len(constants) > 0: # not required to check for prop cases
        bool, arglist1, arglist2 = argumentcheck(s1, s2, predicate_index1, predicate_index2)

        # checks if two returned list have same values/arguments
        for index in range(len(arglist1)):
            if arglist1[index] in constants and arglist2[index] in constants:
                if arglist2[index] == arglist1[index]:

                    continue
                else:
                    return False,[],[]



    # check if both clause has one negation while another not
    negcheck = checknegation(s1, s2, predicate_index1, predicate_index2)


    # if above conditions matches then do resolution on those two clauses
    if negcheck:
        if(resolute(s1, s2, pred)[0]):
            return True,resolute(s1, s2, pred)[1],resolute(s1, s2, pred)[2]
        else:
            return resolute(s1, s2, pred)
    else:
        return False,[],[]



    return True

# comparing each predicate in the clauses
 #- if no predicate found, stop and return false
 # if predicate found in one clause but not in another, stop and return false
 # else return true along with two clauses containing same predicate, and remove those clauses from clause_list
def clauseiterate(e1, e2):
    """
             comparing each predicate in the clauses
             if no predicate found, stop and return false
            if predicate found in one clause but not in another, stop and return false
            else return true along with two clauses containing same predicate, and remove those clauses from clause_list
        """
    counter = 0
    for elements in Predicates:
        predicate_index1 = e1.find(elements)
        predicate_index2 = e2.find(elements)

        if (predicate_index1 >= 0 and predicate_index2 >= 0):
            predicate_value = elements

            return True, [predicate_value, e1, e2]

    return False,[]




def main():
    """
    This is the main program
    """
    global Predicates,variables, constants,functions,clauses
    temp_clauses = clauses
    with open(argv[1]) as f:
        for line in f:
            temp_list = line.strip().split()
            if(temp_list[0] == "Predicates:"):
                Predicates = temp_list[1:]
                #Predicates.add(tmp_Predicates)
            elif (temp_list[0] == "Variables:"):
                variables = temp_list[1:]
            elif (temp_list[0] == "Constants:"):
                constants = temp_list[1:]
            elif (temp_list[0] == "Functions:"):
                functions = temp_list[1:]
            elif (temp_list[0] == "Clauses:"):
                continue
            else:
                clauses.append(line.strip())



    i=0
    clauses_set = set()
    prevc=[]
    fl=False
    while True:
        addset = set()
        removeset = set()
        pairs = combinations(clauses, 2)
        for ele1,ele2 in pairs:

            bool1, s = clauseiterate(ele1,ele2) # s is list of each clause and predicate in common between them


            if bool1 == True:



                if (unificationcheck(s[1], s[2], s[0])[0]):
                    print('No')
                    fl=True
                    break;
                else:
                    for g in unificationcheck(s[1], s[2], s[0])[1]:
                        removeset.add(g);

                    for h in unificationcheck(s[1], s[2], s[0])[2]:
                        addset.add(h);


        i+=1
        if(fl==True):
            break

        for g in removeset:
            clauses.remove(g)

        for h in addset:
            clauses.append(h)
        if prevc==clauses:
            print('Yes')
            break

        prevc=clauses







if __name__ == '__main__':
    # argument check
    if len(sys.argv) == 2:
        main()
    else:
        print("Error! \n It should take 1 argument")