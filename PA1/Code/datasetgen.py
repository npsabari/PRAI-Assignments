import parser
from sets import Set
from mle import get_files

vocab = list()
vocab_size = 0
arff_path = "../arff/"

def arff_gen(strt=0, sz=2, Bern=False):
    global vocab, vocab_size
    # Train set size is 8; Test set size is 2
    name = arff_path+'train'+str(strt)
    if sz == 2: name = arff_path+'test'+str((strt-8+10)%10)
    if Bern: name += '_bern'
    else: name += '_multi'
    # Open the arff file to write
    with open(name+'.arff', 'w') as outfile:
        # arff file initial crazy inputs
        outfile.write('@relation spamset\n\n')
        if not Bern:
            for i in range(vocab_size): outfile.write('@attribute ft'+ str(i)+' numeric\n')
        else:
            for i in range(vocab_size): outfile.write('@attribute ft'+str(i)+' { 0, 1 }\n')
        outfile.write('@attribute spam { yes, no }\n')
        outfile.write('\n@data\n')
        # end of initial crazy inputs
        cnt = 0
        while cnt < sz:
            idx = (cnt+strt)%10
            cnt += 1
            # Get all the files in the folder part+'idx'
            files = get_files(parser.path + 'part' + str(idx))
            for filename in files:
                ns = 'legit' in filename
                # if multinomial we need count
                if not Bern:
                    with open(files[filename]) as infile:
                        word_list = dict()
                        tmp_lst = map(int, str(infile.next()).strip().split()[1:])
                        for line in infile: tmp_lst.extend(map(int, line.strip().split()))
                        for token in tmp_lst:
                            if token in word_list: word_list[token] += 1
                            else: word_list[token] = 1
                    for i in vocab:
                        if i in word_list: outfile.write(str(word_list[i])+', ')
                        else: outfile.write(str(0)+', ')
                # if Bernoulli we just need the boolean value
                else:
                    with open(files[filename]) as infile:
                        word_list = Set(map(int, str(infile.next()).strip().split()[1:]))
                        for line in infile: word_list |= Set(map(int, line.strip().split()))
                    for i in vocab:
                        if i in word_list: outfile.write(str(1)+', ')
                        else: outfile.write(str(0)+', ')
                # last attribute is the class
                if ns: outfile.write('no\n')
                else: outfile.write('yes\n')
    return

def main_arff_gen():
    global vocab, vocab_size
    vocab = list(parser.get_vocab())
    vocab_size = len(vocab)
    for strt in range(0, 10, 2):
        print 'Generating arff for strt = '+str(strt)
        arff_gen(strt, 8, False)
        arff_gen(strt, 8, True)
        arff_gen((strt+8)%10, 2, False)
        arff_gen((strt+8)%10, 2, True)
