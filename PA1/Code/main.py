from parser import main_parser
from mle import multinomial, bernoulli
from bayesian import beta, dirichlet
from datasetgen import main_arff_gen
from sampling import inverse_method, rejective_method

def main():
    # Call this function to parse and collect data
    main_parser()

    # MLE estimates
    multinomial()
    #bernoulli()

    # Bayesian estimates
    #dirichlet()
    #beta()

    # Never run arff gen from now on!
    #main_arff_gen()

    #Uncomment this to demonstrate sampling
    #print inverse_method()
    #print rejective_method()
    return

if __name__ == '__main__':
    main()
