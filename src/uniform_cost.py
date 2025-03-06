from map import Map
from collections import OrderedDict
import time



def sort(d:dict):
    return {i: j for i , j in sorted(d.items(), key = lambda x : x[1])}

def construct_solution(src : str, tgt: str, parents : OrderedDict)->list:
    curr = tgt
    solution= [curr]

    while parents[ curr ] != src:
        solution.append( parents[ curr ])
        curr = parents[ curr ]
    
    solution.append( src )
    solution.reverse()
    
    return solution

def explore_node(
    n : tuple,
    frontier : OrderedDict,
    neighbors : OrderedDict, 
    explored : list,
    parents : OrderedDict
    ) -> None:

    explored.append( n[ 0 ])
    for _ in range( len( neighbors )):
        next = neighbors.popitem( False )

        if next[ 0 ] not in explored:
            parents[ next[ 0 ]] = n[ 0 ]

            if next[ 0 ] not in frontier.keys():
                frontier[ next[ 0 ]] = next[ 1 ] + n[ 1 ]

            elif frontier[ next[ 0 ]] > next[ 1 ] + n[ 1 ]:
                frontier[ next[ 0 ]] = next[ 1 ] + n[ 1 ]

def uniform_cost(
    src : str, 
    tgt : str, 
    m : Map 
    ) -> list :
    """
        src : starting point of search
        tgt : search target
        G : The graph to traverse

        returns a list of the cost and solution to a uniform cost search
    """
    ret = []
    if m.verify(src) and m.verify(tgt):
        explored = []
        frontier = OrderedDict({ src : 0 })
        parents = OrderedDict()
        
        while 1:
            
            frontier = OrderedDict( sort( frontier ))
            n = frontier.popitem( False )
            
            if tgt == n[ 0 ] : 
                ret = [ n[ 1 ], construct_solution( src, tgt, parents ), len(explored)]
                break
            
            neighbors = OrderedDict( sort( m.get_neighbors(n) ))
            explore_node( n, frontier, neighbors, explored, parents ) 

    return ret

def bd_uc(
        src : str,
        tgt : str,
        m : Map
    )->list:
    ret = []

    if m.verify( src ) and m.verify( tgt ):
        explored = []
        
        frontier_alpha = OrderedDict({ src : 0 })
        frontier_omega = OrderedDict({ tgt : 0 })

        parents = OrderedDict()
        #parents_omega = OrderedDict()

        while 1:
            frontier_alpha = OrderedDict( sort( frontier_alpha ))
            frontier_omega = OrderedDict( sort( frontier_omega ))

            n1 = frontier_alpha.popitem( False )
            n2 = frontier_omega.popitem( False )


            if n1[ 0 ] == n2[ 0 ]:
                ret = [n1[1] + n2[1], len(explored)]
                break

            nb_1 = OrderedDict( sort( m.get_neighbors(n1) ))
            nb_2 = OrderedDict( sort( m.get_neighbors(n2) ))

            explore_node(n1, frontier_alpha, nb_1, explored, parents)
            explore_node(n2, frontier_omega, nb_2, explored, parents)

    return ret

if __name__ == "__main__":
    ARAD = 'Arad'
    BUCHAREST = 'Bucharest'


    file_name = "romania.txt"
    

    m = Map( file_name )

    start = time.perf_counter()
    ret = uniform_cost(ARAD, BUCHAREST, m)
    end = time.perf_counter()
    elapsed = end - start

    print(f"uniform cost completed \ntime: {elapsed:.6f}s \nspace: {ret[2]} nodes")

    print('\n')

    start = time.perf_counter()
    ret = bd_uc(ARAD, BUCHAREST, m)
    end = time.perf_counter()
    elapsed = end - start

    print(f"Bi-directional uniform cost completed \ntime: {elapsed:.6f}s \nspace: {ret[1]} nodes")






