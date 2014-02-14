import parser
import os
import math
from sets import Set

# For likelihood
# For Multinomial
vocab_size = 0
vocab = Set()
local_ns_word_count = dict()
local_s_word_count = dict()
local_ns_size = 0
local_s_size = 0

# For Bernoulli
local_ns_word_bool = dict()
local_s_word_bool = dict()

# For prior
docs_ns_size = 0
docs_s_size = 0

def get_files(local_path):
    files = dict()
    for (dirpath, dirnames, filenames) in os.walk(local_path):
        for filename in filenames:
            if filename[-4:] == '.txt':
                files[filename] = os.sep.join([dirpath, filename])
    return files

def update_doc_size(local_path):
    global docs_ns_size, docs_s_size
    for filename in get_files(local_path):
        if 'legit' in filename: docs_ns_size += 1
        else: docs_s_size += 1
    return

def update_local_params(fold, ns=True, count=True):
    main_dict, tmp_dict = dict(), dict()
    global local_ns_word_bool, local_ns_word_count, local_s_word_bool, local_s_word_count
    if ns:
        if count: main_dict, tmp_dict = local_ns_word_count, parser.ns_word_count[fold]
        else: main_dict, tmp_dict = local_ns_word_bool, parser.ns_word_bool[fold]
    else:
        if count: main_dict, tmp_dict = local_s_word_count, parser.s_word_count[fold]
        else: main_dict, tmp_dict = local_s_word_bool, parser.s_word_bool[fold]
    for node in tmp_dict:
        if node in main_dict: main_dict[node] += tmp_dict[node]
        else: main_dict[node] = tmp_dict[node]
    return

def get_vocab_words(strt, Bernoulli=False):
    global local_ns_word_count, local_s_word_count, vocab_size, local_ns_size, local_s_size
    global docs_ns_size, docs_s_size
    global local_ns_word_bool, local_s_word_bool, vocab
    local_ns_word_count = dict()
    local_s_word_count = dict()
    local_ns_word_bool = dict()
    local_s_word_bool = dict()
    vocab = Set()
    local_ns_size, local_s_size, docs_ns_size, docs_s_size = 0, 0, 0, 0
    cnt = 0
    # 5-fold => 8 files are used for training
    while cnt < 8:
        idx = (strt+cnt)%10
        cnt += 1
        # Computing prior probabilities ( Redundant iteration on the files )
        update_doc_size(parser.path+'part'+str(idx)+'/')
        # Computing the likelihood for Multinomial
        if not Bernoulli:
            update_local_params(idx, True, True)
            update_local_params(idx, False, True)
        # Computing likelihood for Bernoulli
        else:
            update_local_params(idx, True, False)
            update_local_params(idx, False, False)
    if not Bernoulli:
        vocab = Set(local_s_word_count.keys()) | Set(local_ns_word_count.keys())
        for token in local_ns_word_count: local_ns_size += local_ns_word_count[token]
        for token in local_s_word_count: local_s_size += local_s_word_count[token]
    else:
        vocab = Set(local_ns_word_bool.keys()) | Set(local_s_word_bool.keys())
    vocab_size = len(vocab)
    print 'Size '+str(vocab_size)
    return

def multinomial():
    global vocab_size, local_ns_size, local_s_size
    global local_ns_word_count, local_s_word_count, docs_ns_size, docs_s_size
    # Crazy Initializations
    true_p = [0 for i in range(5)]
    false_p, true_n, false_n = list(true_p), list(true_p), list(true_p)
    precision, recall, fmeasure, accuracy = list(true_p), list(true_p), list(true_p), list(true_p)
    for strt in range(0, 10, 2):
        get_vocab_words(strt)
        # 5-fold => 2 files are used for testing
        cnt = 0
        while cnt < 2:
            idx = (strt+cnt+8)%10
            cnt += 1
            # Getting all the files to be tested
            files = get_files(parser.path+'part'+str(idx)+'/')
            # Testing phase
            for filename in files:
                tokens = list()
                log_prob_ns = math.log(docs_ns_size*1./(docs_ns_size+docs_s_size))
                log_prob_s = math.log(docs_s_size*1./(docs_ns_size+docs_s_size))
                ns = 'legit' in filename
                # Accumulating all the tokens in a list (not in a set)
                with open(files[filename], 'r') as infile:
                    tokens.extend(map(int, str(infile.next()).strip().split()[1:]))
                    for line in infile: tokens.extend(map(int, line.strip().split()))
                # Adding MAP log probabilities
                for token in tokens:
                    t = 0
                    if token in local_ns_word_count: t = local_ns_word_count[token]
                    log_prob_ns += math.log((t+1.)/(local_ns_size+vocab_size))
                    t = 0
                    if token in local_s_word_count: t = local_s_word_count[token]
                    log_prob_s += math.log((t+1.)/(local_s_size+vocab_size))
                #print 'log_ns %f, log_s %f' % (log_prob_ns, log_prob_s)
                # Classified as spam
                if log_prob_ns <= log_prob_s:
                    if ns: false_p[strt>>1] += 1
                    else: true_p[strt>>1] += 1
                # Classified as non-spam
                else:
                    if ns: true_n[strt>>1] += 1
                    else: false_n[strt>>1] += 1

        # Calculating precision, recall and f-measure
        precision[strt>>1] = (true_p[strt>>1]*1.)/(true_p[strt>>1] + false_p[strt>>1])
        recall[strt>>1] = (true_p[strt>>1]*1.)/(true_p[strt>>1] + false_n[strt>>1])
        fmeasure[strt>>1] = (precision[strt>>1]*recall[strt>>1])/(precision[strt>>1]+recall[strt>>1])*2.0
        accuracy[strt>>1] = (true_p[strt>>1]+true_n[strt>>1])*1./ \
                (true_p[strt>>1]+true_n[strt>>1]+false_p[strt>>1]+false_n[strt>>1])

    # Printing the calculated values
    for i in range(len(precision)):
        print 'accuracy %f, precision %f, recall %f, fmeasure %f' \
        % (accuracy[i], precision[i], recall[i], fmeasure[i])

def bernoulli():
    global vocab_size, docs_ns_size, docs_s_size
    global local_ns_word_bool, local_s_word_bool, vocab
    # Crazy Initializations
    true_p = [0 for i in range(5)]
    false_p, true_n, false_n = list(true_p), list(true_p), list(true_p)
    precision, recall, fmeasure, accuracy = list(true_p), list(true_p), list(true_p), list(true_p)
    for strt in range(0, 10, 2):
        get_vocab_words(strt, True)
        # 5-fold => 2 files are used for testing
        cnt = 0
        while cnt < 2:
            idx = (strt+cnt+8)%10
            cnt += 1
            # Getting all the files to be tested
            files = get_files(parser.path+'part'+str(idx)+'/')
            # Testing phase
            for filename in files:
                tokens = Set()
                log_prob_ns = math.log(docs_ns_size*1./(docs_ns_size+docs_s_size))
                log_prob_s = math.log(docs_s_size*1./(docs_ns_size+docs_s_size))
                ns = 'legit' in filename
                # Accumulating all the tokens in a list (not in a set)
                with open(files[filename], 'r') as infile:
                    tokens |= Set(map(int, str(infile.next()).strip().split()[1:]))
                    for line in infile: tokens |= Set(map(int, line.strip().split()))
                # Adding MAP log probabilities
                for token in vocab:
                    present = token in tokens
                    t = 0
                    if token in local_ns_word_bool: t = local_ns_word_bool[token]
                    val = (t+1.)/(docs_ns_size+2)
                    if present: log_prob_ns += math.log(val)
                    else: log_prob_ns += math.log(1.-val)
                    t = 0
                    if token in local_s_word_bool: t = local_s_word_bool[token]
                    val = (t+1.)/(docs_s_size+2)
                    if present: log_prob_s += math.log(val)
                    else: log_prob_s += math.log(1.-val)
                #print 'log_ns %f, log_s %f' % (log_prob_ns, log_prob_s)
                # Classified as spam
                if log_prob_ns <= log_prob_s:
                    if ns: false_p[strt>>1] += 1
                    else: true_p[strt>>1] += 1
                # Classified as non-spam
                else:
                    if ns: true_n[strt>>1] += 1
                    else: false_n[strt>>1] += 1

        # Calculating precision, recall and f-measure
        precision[strt>>1] = (true_p[strt>>1]*1.)/(true_p[strt>>1] + false_p[strt>>1])
        recall[strt>>1] = (true_p[strt>>1]*1.)/(true_p[strt>>1] + false_n[strt>>1])
        fmeasure[strt>>1] = (precision[strt>>1]*recall[strt>>1])/(precision[strt>>1]+recall[strt>>1])*2.0
        accuracy[strt>>1] = (true_p[strt>>1]+true_n[strt>>1])*1./ \
                (true_p[strt>>1]+true_n[strt>>1]+false_p[strt>>1]+false_n[strt>>1])

    # Printing the calculated values
    for i in range(len(precision)):
        print 'accuracy %f, precision %f, recall %f, fmeasure %f' \
        % (accuracy[i], precision[i], recall[i], fmeasure[i])
