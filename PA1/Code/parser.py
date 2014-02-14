import os
from sets import Set

ns_word_count = [dict() for i in range(10)]
s_word_count = [dict() for i in range(10)]
ns_word_bool = [dict() for i in range(10)]
s_word_bool = [dict() for i in range(10)]
list_of_files = [dict() for i in range(10)]
path = '../Data/'

def get_all_files():
    global list_of_files, path
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            if filename[-4:] == '.txt':
                list_of_files[int(dirpath[-1:])][filename] = os.sep.join([dirpath, filename])
    return list_of_files

def add_to_dict(main_dict, lst, fold):
    for e in lst:
        if main_dict[fold].has_key(e): main_dict[fold][e] += 1
        else: main_dict[fold][e] = 1
    return

def main_parser():
    global s_word_count, ns_word_count, list_of_files, ns_word_bool, s_word_bool
    for idx, fold in enumerate(get_all_files()):
        for filename in fold:
            with open(fold[filename], 'r') as infile:
                unique_token = Set()
                ns = 'legit' in filename
                # Not-spam emails
                if ns:
                    tmp_lst = map(int, str(infile.next()).strip().split()[1:])
                    unique_token |= Set(tmp_lst)
                    add_to_dict(ns_word_count, tmp_lst, idx)
                    for line in infile:
                        tmp_lst = map(int, line.strip().split())
                        add_to_dict(ns_word_count, tmp_lst, idx)
                        unique_token |= Set(tmp_lst)
                    add_to_dict(ns_word_bool, unique_token, idx)
                # Spam emails
                else:
                    tmp_lst = map(int, str(infile.next()).strip().split()[1:])
                    unique_token |= Set(tmp_lst)
                    add_to_dict(s_word_count, tmp_lst, idx)
                    for line in infile:
                        tmp_lst = map(int, line.strip().split())
                        add_to_dict(s_word_count, tmp_lst, idx)
                        unique_token |= Set(tmp_lst)
                    add_to_dict(s_word_bool, unique_token, idx)
    return
