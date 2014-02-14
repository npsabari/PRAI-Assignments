from parser import main_parser
from naivebayes import multinomial, bernoulli

def main():
    main_parser()
    multinomial()
    bernoulli()
    return

if __name__ == '__main__':
    main()
