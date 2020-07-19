import matplotlib.pyplot as plt
import networkx as nx
from os import listdir, getcwd, remove
import imageio
from re import sub

def DrawTheGrap(G,i,j):
    #Obtain Position of the nodes
    pos=nx.get_node_attributes(G,'pos')
    #Draw the nodes with a node size of 100
    nx.draw_networkx_nodes(G, pos, node_size=100)
    #The weights are saved in a convenient Dict
    labels = nx.get_edge_attributes(G,'weight')
    #Draw the edge set with thin lines
    nx.draw_networkx_edges(G, pos,width=1)
    #Draw the weights on the corresponding edges
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    # labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
    
    plt.axis('off')
    #plt.figure(figsize=(1,1))
    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    #plt.title('Updated at Step:' + str(j))
    plt.savefig(str(i) + '.png')
    plt.clf()
    return

def ChooseyTravsChooseGIF():
    images = []
    pngs = [file for file in listdir(getcwd()) if '.png' in file]
    pngs.sort(key=lambda f: int(sub('\D', '', f)))
    for file in pngs:
        if '.png' in file:
            #Take all of the png's generated above and form a GIF
            images.append(imageio.imread(file))
            remove(file)
    imageio.mimsave('ReverseDelete.gif', images, format='GIF', duration=2)
    return

def TellMeNow(outputFile, step, edge, Connected):
    if Connected:
        outputFile.write('Step ' + str(step) + ' tried deleting the edge from ' + edge[0] + ' to ' + edge[1] + ' with weight ' + str(edge[2]['weight']) + ' and this results in a connected graph, so it shall be removed\n')
    else:
        outputFile.write('Step ' + str(step) + ' tried deleting the edge from ' + edge[0] + ' to ' + edge[1] + ' with weight ' + str(edge[2]['weight']) + ' and this results in a disconnected graph, so it shall not be removed\n')
    return

def ReverseDelete(G):
    H = G.copy()
    numGifs = 1
    steps = 1
    outputFile = open('ReverseDeleteSteps.txt', 'a+')
    for TestEdge in sorted(G.edges(data=True), key=lambda t: t[2].get('weight', 1), reverse = True):
        H.remove_edge(TestEdge[0],TestEdge[1])
        if nx.is_connected(H):
            G = H.copy()
            DrawTheGrap(H,numGifs,steps)
            TellMeNow(outputFile, steps, TestEdge, True)
            numGifs+=1
            steps+=1
        else:
            H = G.copy()
            TellMeNow(outputFile, steps, TestEdge, False)
            steps+=1
    outputFile.close()
    return

def ParseTheConfig():
    Config = open('config.txt', 'r+')
    lines = Config.readlines()
    Nodes, Edges = ([] for i in range(2))
    for line in lines:
        line = line.strip().split(',')
        if 'node' in line[0]:
            Nodes.append(line[1:])
        elif 'edge' in line[0]:
            Edges.append(line[1:])
    return Nodes,Edges

def main():
    Nodes,Edges = ParseTheConfig()
    G = nx.Graph()
    [G.add_node(node[0], pos=(float(node[1]),float(node[2]))) for node in Nodes]
    [G.add_edge(edge[0], edge[1]) for edge in Edges]
    #[G.add_edge(edge[0], edge[1], weight = edge[2]) for edge in Edges]

    DrawTheGrap(G,0,0)
    #ReverseDelete(G)
    #ChooseyTravsChooseGIF()
    return


main()