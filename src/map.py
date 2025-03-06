# Author : barnon_H

# ########### Imports #################
import networkx as nx
import argparse
import matplotlib.pyplot as plt
from networkx.classes import Graph





class Map:

    def __init__(self, file_name : str ):
        self.WEIGHT = "weight"
        self.f_name = file_name
        self.vertices_and_edges, self.coordinates = self._read_file(self.f_name)
        self.g = self._create_graph(self.vertices_and_edges)

    def _read_line(self,  
                   line : str,
                   vertices_and_edges : list,
                   coordinates : dict
                   )->None:
        source, target, distance, x1, y1, x2, y2 = line.split(",")
                    
        src = source.strip()
        tgt = target.strip()
                    
        vertices_and_edges.append(( src, tgt, float( distance )))

        if src not in coordinates.keys():
            coordinates[ src ] = ( float( x1 ), float( y1 ))

        if tgt not in coordinates.keys():
            coordinates[ tgt ] = ( float( x2 ), float( y2 ))


    def _read_file(self,  f_name : str ):
            """
            input : name of file
            Reads a csv formatted file and 
            returns a list of vertices with weighted edges
            """
            vertices_and_edges = []
            coordinates = {}

            with open( f_name, "r" ) as file:
                for i in file:
                    if i[ 0 ].strip() != '#' and i != '\n':
                        try:
                            self._read_line(i, vertices_and_edges, coordinates)                            
                        except:
                            print("Illegal File")
                            quit()
    
            return [vertices_and_edges, coordinates]

    def _create_graph(self, vertices_and_edges : list ) -> nx.Graph:
        """
            creates a weighted graph using networkx
        """
        g = Graph()
        g.add_weighted_edges_from(vertices_and_edges)
    
        return g

    def verify(self, src : str ) -> bool:
        return src in self.g.nodes

    def get_neighbors( self, src )->dict:
        ret = {}
        if self.verify(src[ 0 ]):
            ret = { i : self.g.get_edge_data( src[0], i)[ self.WEIGHT ] for i in nx.neighbors( self.g,src[ 0 ])}
        return ret

    def draw_solution(self, 
                      solution, 
                      )-> None:

        l = [(solution[ i ],solution[ i + 1 ]) for i in range(len(solution)-1)]
        
        nx.draw_networkx_nodes(self.g, self.coordinates, nodelist=self.g.nodes(),node_color="tab:blue", node_size=100)
        nx.draw_networkx_nodes(self.g, self.coordinates, nodelist=solution, node_color="tab:red", node_size=100)

        nx.draw_networkx_edges(self.g, self.coordinates)
        nx.draw_networkx_edges(
            self.g,
            self.coordinates,
            edgelist=l,
            width = 3,
            edge_color = "tab:red")

        coords = [ self.coordinates[i] for i in solution]
        s = {i:solution[i] for i in range(len(solution))}
        nx.draw_networkx_labels(self.g, coords,  s, font_size= 10)
    
        plt.title("solution")
        plt.savefig("solution.jpg", dpi = 300)
        plt.close()

    def draw_map(self,
                 filename :str,
                 g : nx.Graph,
                 pos
                 ) -> None:
        """
            draws a graph and 
        """
        nx.draw(g, pos, with_labels=True)

        plt.title(filename)
        plt.savefig("out.jpg", dpi = 300)
        plt.close()




# ############# Main ###################
def main( filename : str ) -> None:
    m = Map(filename)
    print(m.get_neighbors(("Arad",0)))
    m.draw_solution(solution= ["Arad", "Sibiu", "Rimnicu Vilcea", "Pitesti", "Bucharest"]) 

# ########## Driver Code ###############
if __name__ == "__main__":
    parser = argparse.ArgumentParser( prog = "map.py" )
    parser.add_argument( 'filename' )
    args = parser.parse_args()
    
    main( args.filename )
