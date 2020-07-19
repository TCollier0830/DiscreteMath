import networkx as nx
import matplotlib.pyplot as plt
from numpy import linspace
from os import listdir, getcwd, remove
import imageio

def Existence(deg_seq):
    #Corollary of of Theorem 1.1 is that an odd degree sequence can't define a graph.
    if sum(deg_seq) % 2:
        return False
    #Theorem proved in class
    for k in range(1,len(deg_seq) + 1):
        left = sum(deg_seq[:k])
        right =  k * (k-1) + sum([min(x,k) for x in deg_seq[k:]])
        if left > right:
            return False
    return True

def FindGraph(deg_seq, MakeGIF, cycle, num, noplotting):
    #After having done these by hand I wanted to find an algorithmic way of doing it.
    #That desire culminated in me finding this paper on Arxiv: https://arxiv.org/pdf/cs/0702124.pdf
    #The algorithm described in that paper was implemented in the python library networkx.
    #The goal then is to take the networkx implementation and making an animated "growth"
    #that would enable one to pick out different patterns.
    #More on the networkx library can be found here:
    #https://networkx.github.io/documentation/networkx-2.0
    n = num+1
    for seq in deg_seq:
        seq.sort(reverse=True)
        exists = Existence(seq)
        if exists == False:
            print(exists)
        if(exists) and noplotting==False:
            if cycle:
                #The algorithm for this is described in the homework.
                G = nx.cycle_graph(n)
            else:
                #Since the algorithm is randomly seeded it has a failure rate directly proportional to n,
                #thus we should give it a number of tries proportional to n, 3n seems to be a good guess.
                G = nx.random_degree_sequence_graph(seq, tries=3*n)
            plt.title('n: ' + str(n))
            if len(seq) > 70:
                #This is a quality of life feature so the screen isn't crowded by numbers.
                #Further, the node size should be a monotonically decreasing function of the number of nodes
                #so that the picture isn't just a big splotch of blue.
                nx.draw_circular(G, with_labels=False, node_size=800/(n/2))
            else:
                nx.draw_circular(G, with_labels=True, node_size=800/(n/2))
            #Formatting to save as nnnnnnnn.png
            plt.savefig(str(len(seq)).replace(',','').replace('[','').replace(']','').replace(' ','')+'.png')
            #pyplot is dumb and doesn't realize that it should clear itself after it's been saved.
            plt.clf()
        n+=1
    if MakeGIF and noplotting==False:
        images = []
        for file in listdir(getcwd()):
            if '.png' in file:
                #Take all of the png's generated above and form a GIF
                images.append(imageio.imread(file))
                remove(file)
        imageio.mimsave('GrowthBy' + str(num) + '.gif', images, duration=min(30/(n-num-1),.5))
        return

def Tree():
    try:
        import pygraphviz
        from networkx.drawing.nx_agraph import graphviz_layout
    except ImportError:
        try:
            import pydot
            from networkx.drawing.nx_pydot import graphviz_layout
        except ImportError:
            raise ImportError("This example needs Graphviz and either "
                              "PyGraphviz or pydot")


    G = nx.balanced_tree(3, 3)
    plt.figure(figsize=(8, 8))
    nx.draw(G, node_size=20, alpha=0.5, node_color="blue", with_labels=False)
    plt.axis('equal')
    plt.show()
    return

##INPUT
#sequences = []
##sequences = [[3,4,3,3,1], [6,6,5,4,4,3], [4,4,4,4,3,3,3,3], [3,1,1,1,1,1]]
#noplotting = False
#cycle = False
#MakeGif = False
#num = 7
#max_num_frames = 200
#if num == 2:
#    cycle = True
#
#for n in range(num+1,max_num_frames):
#    sequences.append([num] * n)
#    MakeGif = True
#    
#
#FindGraph(sequences, MakeGif, cycle, num, noplotting)

Tree()