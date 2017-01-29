import sys
import os
import re
import pprint

my_first_pat =  "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)" #'(\w+) @ (\w+).edu|(\w+)@(\w+).edu|(\w\S+)@(\w\S+).(\w+)'
my_pat_1 = '(?:(\d{3})[-. ](\d{3})[-. ](\d{4})|\((\d{3})\) (\d{3})-(\d{4})|\((\d{3})\)(\d{3})-(\d{4}))'
myPatternWithSpace = "(^[a-zA-Z0-9_.+-] +@ [a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


"""
TODO
This function takes in a filename along with the file object (actually
a StringIO object) and
scans its contents against regex patterns. It returns a list of
(filename, type, value) tuples where type is either an 'e' or a 'p'
for e-mail or phone, and value is the formatted phone number or e-mail.
The canonical formats are:
     (name, 'p', '###-###-#####')
     (name, 'e', 'someone@something')
If the numbers you submit are formatted differently they will not
match the gold answers

NOTE: ***don't change this interface***

NOTE: You shouldn't need to worry about this, but just so you know, the
'f' parameter below will be of type StringIO. So, make
sure you check the StringIO interface if you do anything really tricky,
though StringIO should support most everything.
"""
def process_file(name, f):
    # note that debug info should be printed to stderr
    # sys.stderr.write('[process_file]\tprocessing file: %s\n' % (path))
    print "------\n\n\n"
    print name
    res = []
    for line in f:

        #A tricky method: find if there is an <a> tag with email link starting with 'mailto:'
        splitedResult = line.split('mailto:')
        if len(splitedResult) > 1:
            result2 = splitedResult[1].split('\"')
            #print result2[0]
            res.append((name,'e',result2[0]))

        #Brute-force for dlwh data:

        elif len(line.split('-'))>10:
            normal = "".join(line.strip().split('-'))
            match = re.findall(my_first_pat,normal)

            if len(match)>0:
                res.append((name,'e',match[0]))

        else:
            matches_1 = re.findall(my_first_pat,line.strip())


            if len(matches_1)!=0:
                #print matches_1
                pass

            for m in matches_1:
                #print m
                ln1 = " ".join(m).split()
                ln1.insert(1,"@")
                ln1.insert(3,".edu")
                #print "".join(ln1)
                res.append((name,'e',"".join(ln1)))


        #phone number processing
        matches_2 = re.findall(my_pat_1,line.strip())

        for n in matches_2:
            ln = list("".join(list(n)))
            ln.insert(3,"-")
            ln.insert(7,"-")
            res.append((name,'p',"".join(ln)))
    return res

"""
You should not need to edit this function, nor should you alter
its interface
"""
def process_dir(data_path):
    # get candidates
    guess_list = []
    for fname in os.listdir(data_path):
        if fname[0] == '.':
            continue
        path = os.path.join(data_path,fname)
        f = open(path,'r')
        f_guesses = process_file(fname, f)
        guess_list.extend(f_guesses)
    return guess_list

"""
You should not need to edit this function.
Given a path to a tsv file of gold e-mails and phone numbers
this function returns a list of tuples of the canonical form:
(filename, type, value)
"""
def get_gold(gold_path):
    # get gold answers
    gold_list = []
    f_gold = open(gold_path,'r')
    for line in f_gold:
        gold_list.append(tuple(line.strip().split('\t')))
    return gold_list

"""
You should not need to edit this function.
Given a list of guessed contacts and gold contacts, this function
computes the intersection and set differences, to compute the true
positives, false positives and false negatives.  Importantly, it
converts all of the values to lower case before comparing
"""
def score(guess_list, gold_list):
    guess_list = [(fname, _type, value.lower()) for (fname, _type, value) in guess_list]
    gold_list = [(fname, _type, value.lower()) for (fname, _type, value) in gold_list]
    guess_set = set(guess_list)
    gold_set = set(gold_list)

    tp = guess_set.intersection(gold_set)
    fp = guess_set - gold_set
    fn = gold_set - guess_set

    pp = pprint.PrettyPrinter()
    #print 'Guesses (%d): ' % len(guess_set)
    #pp.pprint(guess_set)
    #print 'Gold (%d): ' % len(gold_set)
    #pp.pprint(gold_set)
    print 'True Positives (%d): ' % len(tp)
    pp.pprint(tp)
    print 'False Positives (%d): ' % len(fp)
    pp.pprint(fp)
    print 'False Negatives (%d): ' % len(fn)
    pp.pprint(fn)
    print 'Summary: tp=%d, fp=%d, fn=%d' % (len(tp),len(fp),len(fn))

"""
You should not need to edit this function.
It takes in the string path to the data directory and the
gold file
"""
def main(data_path, gold_path):
    guess_list = process_dir(data_path)
    gold_list =  get_gold(gold_path)
    score(guess_list, gold_list)

"""
commandline interface takes a directory name and gold file.
It then processes each file within that directory and extracts any
matching e-mails or phone numbers and compares them to the gold file
"""
if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print 'usage:\tSpamLord.py <data_dir> <gold_file>'
        sys.exit(0)
    main(sys.argv[1],sys.argv[2])
