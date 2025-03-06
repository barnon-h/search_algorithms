from uniform_cost import uniform_cost
from uniform_cost import bd_uc
from a_search import a_star
from a_search import bd_as

from map import Map
from time import perf_counter



class test:

    def __init__(self):
        pass



def main()->None:
    t = test()
    
    ARAD  = 'Arad'
    BUCHAREST = 'Bucharest'

    romania = Map( 'romania.txt' )

    print(f"{'*' * 55}\n\t\tExecuting runtime tests\n{'*' * 55}\n")

    start = perf_counter()
    uc = uniform_cost( ARAD, BUCHAREST, romania )
    end = perf_counter()
    elapsed = end - start

    print( f"unifrom cost search executed \nt : {elapsed:.6f}(s) space : {uc[2]}(n)\n")

    start = perf_counter()
    res = bd_uc( ARAD, BUCHAREST, romania)
    end = perf_counter()
    elapsed = end - start

    print( f"bidirectional unifrom cost search executed \nt : {elapsed:.6f}(s) space : {res[1]}(n)\n")


    start = perf_counter()
    res = a_star( ARAD, BUCHAREST, romania)
    end = perf_counter()
    elapsed = end - start

    print( f"A-Star search executed \nt : {elapsed:.6f}(s) space : {res[1]}(n)\n")

    start = perf_counter()
    res = bd_as( ARAD, BUCHAREST, romania)
    end = perf_counter()
    elapsed = end - start

    print( f"bi-directional A-Star search executed \nt : {elapsed:.6f}(s) space : {res[1]}(n)\n")



if __name__ == "__main__":
    main()
