from collections.abc import Callable
from map import Map
import heapq as pq

h = 0
key = 1
dist = 2

def euclidean( x1 : list, x2 : list ) -> float:
    from math import sqrt
    if len( x1 ) == len( x2 ):
        return sqrt( sum( (x1[ i ] - x2[ i ]) ** 2 for i in range( len( x1 ))))
    return 0.0

def h_euclidean( src : list, tgt :str , m : Map )-> float:
    """
        h(n) = euclidean( src, tgt )
    """
    src_coords = m.coordinates[ src[ 0 ]]
    tgt_coords = m.coordinates[ tgt ]
    
    h_n = euclidean( src_coords, tgt_coords )
    
    return h_n


def h_manhattan( src, tgt )-> float:
    return 0.0

def bd_as(
        src : str,
        tgt : str,
        m : Map, 
        h : Callable = h_euclidean
    )->list:
    
    f = False
    ret = []
    intersection = None

    if m.verify( src ) and m.verify( tgt ):
        frontier_alpha = [[ 0, src, 0]]
        frontier_omega = [[ 0, tgt, 0]]

        explored = []
        parents = {}

        while 1:
            n1 = pq.heappop( frontier_alpha )
            n2 = pq.heappop( frontier_omega )

            neighbors_n1 = m.get_neighbors( n1[ 1: ])
            neighbors_n2 = m.get_neighbors( n2[ 1: ])


            for i in neighbors_n1.keys():
                if i in neighbors_n2.keys():
                    intersection = i
            
            if intersection:
                cost = n1[ 2 ] + n2[ 2 ] + neighbors_n1[intersection] + neighbors_n2[intersection]
                explored.append(intersection)
                explored.append(n1[1])
                explored.append(n2[1])
                ret = [cost, len(explored)]
                break

            neighbors_n1 = [[ i, neighbors_n1[ i ]] for i in neighbors_n1 ]
            neighbors_n2 = [[ i, neighbors_n2[ i ]] for i in neighbors_n2 ]


            hn_n1 = [[ h( i, tgt, m) + i[ 1 ], i[ 0 ], i[ 1 ]] for i in neighbors_n1 ]
            hn_n2 = [[ h( i, src, m) + i[ 1 ], i[ 0 ], i[ 1 ]] for i in neighbors_n2 ]

            explore_node( n1, hn_n1, explored, frontier_alpha, parents)
            explore_node( n2, hn_n2, explored, frontier_omega, parents)

    return ret


def a_star(
        src : str, 
        tgt : str, 
        m : Map, 
        h : Callable = h_euclidean 
    )-> list:

    """
        A-star search algorithm
        f(n) = g(n) + h(n)
    """
    ret = []

    if m.verify( src ) and m.verify( tgt ):
        parents = {}
        frontier = [[0, src, 0]]
        explored = []
        
        while 1:
            n = pq.heappop( frontier )

            if n[1] == tgt:
                explored.append( n[ 1 ])
                ret = [ n[ 2 ] , len( explored )]
                break

            neighbors = m.get_neighbors( n[ 1: ])
            neighbors = [[ i, neighbors[ i ]] for i in neighbors ] 
            
            h_neighbors = [[ h( i, tgt, m ) + i[ 1 ], i[ 0 ], i[ 1 ]] for i in neighbors ]
            explore_node( n, h_neighbors, explored, frontier, parents )

    return ret


def explore_node(
        n :list, 
        neighbors: list, 
        explored : list, 
        frontier : list,
        parents : dict
        ) -> None:
    
    explored.append( n[ 1 ])

    pq.heapify( neighbors )
    for _ in range( len( neighbors )):
        next = pq.heappop( neighbors )
        
        if next[ key ] not in explored:
            parents[ next[ key ]] = n[ key ]

            if next[ key ] not in [ i[ key ] for i in frontier]:
                
                next[ dist ] += n[ dist ]
                pq.heappush( frontier, next )
            
            else:    
                for i in frontier:
                    
                    if i[ key ] == next[ key ] and i[ h ] > next[ h ]:
                        i[ h ] = next[ h ]
                        i[ dist ] = next[ dist ] + n[ dist ]






def main()-> None:
    fname = "romania.txt"

    ARAD = 'Arad'
    BUCHAREST = "Bucharest"

    m = Map( fname )

    ret = bd_as( ARAD, BUCHAREST, m )
    print( ret )

    pass

if __name__ == "__main__":
    main()
