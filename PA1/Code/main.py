from parser import main_parser
from naivebayes import multinomial, bernoulli
from datasetgen import main_arff_gen
from sampling import inverse_method, rejective_method

def main():
    #main_parser()
    #multinomial()
    #bernoulli()
    # Never run arff gen from now on!
    #main_arff_gen()
    print inverse_method()
    print rejective_method()
    return

if __name__ == '__main__':
    main()
