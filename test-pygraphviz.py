import tkinter as tk
from tkinter import DoubleVar, filedialog
from tkinter import ttk
import pygraphviz as pgv
from PIL import Image, ImageTk
import community
from pygraphviz import AGraph
import networkx as nx
import numpy as np
from community import community_louvain
import matplotlib.pyplot as plt
from fa2 import ForceAtlas2

# Créez la fenêtre principale
window = tk.Tk()
window.title("Visualisation de graphe")
positions = None
G = None
node_colors = None
node_sizes = None
comms = None
# Créez un bouton "Ouvrir fichier"

def open_file():
    filepath = filedialog.askopenfilename()
    # Appelez la fonction de dessin du graphe ici en passant filepath comme argument
    p = start_graph(filepath)

def validate(P):
    if P.isdigit():
        return True
    if P == "":
        return True
    try:
        float(P)
        return True
    except ValueError:
        return False

def start_graph(filepath):
    global positions
    positions = None 
    global node_colors
    node_colors = None 
    global node_sizes 
    node_sizes = None
    global comms 
    comms = None
    # Chargez le fichier .dot dans un objet Graph
    graph = pgv.AGraph(filename=filepath)
    g = graph.to_undirected()
    global G 
    G = nx.nx_agraph.from_agraph(g)
    # Déterminez les clusters du graphe en utilisant la méthode de Louvain
    #partition = community.best_partition(g)

    # Affichez les clusters en ajoutant des couleurs aux noeuds du graphe
    #for node, cluster in partition.items():
    #    graph.get_node(node).attr['style'] = f'filled'
    #    graph.get_node(node).attr['fillcolor'] = f'#{cluster:x}'
    forceatlas2 = ForceAtlas2(
        # Behavior alternatives
        outboundAttractionDistribution=True,  # Dissuade hubs
        linLogMode=False,  # NOT IMPLEMENTED
        adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
        edgeWeightInfluence=1.0,

        # Performance
        jitterTolerance=1.0,  # Tolerance
        barnesHutOptimize=True,
        barnesHutTheta=10.0,
        multiThreaded=False,  # NOT IMPLEMENTED

        # Tuning
        scalingRatio=float(entry1.get()),
        strongGravityMode=False,
        gravity=float(entry.get()),

        # Log
        verbose=True) 

    positions = forceatlas2.forceatlas2_networkx_layout(G, pos=positions, iterations=50)

    comms = community_louvain.best_partition(G)

    unique_coms = np.unique(list(comms.values()))
    #print(len(unique_coms))
    global combo2
    combo2 = ttk.Combobox(window, values=[i for i in range(len(unique_coms))])
    combo2.current(0)  # set the selected item
    combo2.grid(row=4,column=1)
    cmap = {
        0: 'red',
        1: 'teal',
        2: 'yellow',
        3: 'purple',
        4: 'orange',
        5: 'black',
        6: 'blue'
    }

    node_colors = [cmap[v % 7] for _, v in comms.items()]

    #print(comms)
    # Create a colormap with a random color for each group
    #cmap = plt.get_cmap("Set1")
    #colors = [cmap(i) for i in np.linspace(0, 1, len(np.unique(list(comms.values()))))]

    # Create a list of colors for each node, based on their group ID
    #node_colors = [colors[v] for _, v in comms.items()] 

    # Create a dictionary to map group IDs to shapes
    shape_map = {
        0 : 'o',#forme de cercle (par défaut)
        1 : 's', #forme de carré
        2 : '^', #forme de triangle pointant vers le haut
        3 : 'v', #forme de triangle pointant vers le bas
        4 : '<', #forme de triangle pointant vers la gauche
        5 : '>', #forme de triangle pointant vers la droite
        6 : 'd', #forme de losange
        7 : 'p', #forme de pentagone
        8 : 'h', #forme de hexagone
        9 : '8', #forme de octogone
        10 : '+', #forme de croix
        11 : 'X' #forme de x
    }

    # Create a list of shapes for each node, based on their group ID
    node_shapes = [shape_map[v % 12] for _, v in comms.items()]

    #fig = plt.figure(facecolor='darkgrey')

    # Créez un objet Figure et un objet Axes
    #figure, ax = plt.subplots()
    #ax = fig.add_subplot(1, 1, 1)


    # Récupérez les degrés de tous les noeuds
    degrees = dict(G.degree())

    # Définissez la taille des noeuds en fonction de leur degré
    node_sizes = [((v/10) + 1) * 20 for v in degrees.values()]

def dessiner_graphe():
    global positions 
    global node_colors
    global node_sizes
    global comms
    global G

    if(G == None):
        return Exception

    forceatlas2 = ForceAtlas2(
        # Behavior alternatives
        outboundAttractionDistribution=True,  # Dissuade hubs
        linLogMode=False,  # NOT IMPLEMENTED
        adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
        edgeWeightInfluence=1.0,

        # Performance
        jitterTolerance=10,  # Tolerance
        barnesHutOptimize=True,
        barnesHutTheta=5.0,
        multiThreaded=False,  # NOT IMPLEMENTED

        # Tuning
        scalingRatio=5.0,
        strongGravityMode=False,
        gravity=1.,

        # Log
        verbose=True) 

    positions = forceatlas2.forceatlas2_networkx_layout(G, pos=positions, iterations=int(combo1.get()))
    cmap = {
        0: 'red',
        1: 'teal',
        2: 'yellow',
        3: 'purple',
        4: 'orange',
        5: 'black',
        6: 'blue'
    }
    i=0
    for _,v in comms.items():
        if v == int(combo2.get()):
            node_colors[i]= combo4.get()
        i=i+1
    #node_colors = [combo4.get() if ((v%7)==int(combo2.get())) else node_colors[int(i)] for i, v in comms.items()]
    #print(node_colors[1])
    #print(combo2.get())
    # Dessinez le graphe
    nx.draw_networkx_edges(G, positions, edge_color="black", alpha=1, style='dashed')
    #for node in G.nodes():
    #    value = int(node)
    #    print(value)
    #    nx.draw_networkx_nodes(G, positions, nodelist=[node], node_size=node_sizes[value], node_color=node_colors[value], node_shape=node_shapes[value], alpha= 0.8)
    nx.draw_networkx_nodes(G, positions, node_size=node_sizes, node_color=node_colors,node_shape= combo3.get(), alpha =0.8)
    #print(positions)
    #print("\n")
    #nx.draw(G, positions, with_labels=False)
    #x = [t[0] for t in positions.values()]
    #y = [t[1] for t in positions.values()]

    # Définissez les limites de l'axe des x et des y pour zoomer sur une partie du graphe
    #ax.set_xlim(min(x) - 1000, max(x) + 1000)
    #ax.set_ylim(min(y) - 1000, max(y) + 1000)

    # Enregistrer les données de positions dans un fichier CSV
    #np.savetxt("positions.csv", np.array(list(positions.values())), delimiter=",")  

    # Masquez les axes
    plt.axis('off')

    # Enregistrer la figure au format SVG
    #plt.savefig("figure.svg")

    # Affichez la figure
    plt.show()

def SaveSVG():
    # Dessinez le graphe
    nx.draw_networkx_edges(G, positions, edge_color="black", alpha=1, style='dashed')
    #for node in G.nodes():
    #    value = int(node)
    #    print(value)
    #    nx.draw_networkx_nodes(G, positions, nodelist=[node], node_size=node_sizes[value], node_color=node_colors[value], node_shape=node_shapes[value], alpha= 0.8)
    nx.draw_networkx_nodes(G, positions, node_size=node_sizes, node_color=node_colors,node_shape= combo3.get(), alpha =0.8)
    #print(positions)
    #print("\n")
    #nx.draw(G, positions, with_labels=False)
    #x = [t[0] for t in positions.values()]
    #y = [t[1] for t in positions.values()]

    # Définissez les limites de l'axe des x et des y pour zoomer sur une partie du graphe
    #ax.set_xlim(min(x) - 1000, max(x) + 1000)
    #ax.set_ylim(min(y) - 1000, max(y) + 1000)

    # Enregistrer les données de positions dans un fichier CSV
    #np.savetxt("positions.csv", np.array(list(positions.values())), delimiter=",")  

    # Masquez les axes
    plt.axis('off')

    # Enregistrer la figure au format SVG
    plt.savefig(entrySVG.get())

lab1 = ttk.Label(window, text="parametres fa2 à selectionner avant l'ouverture du fichier:")
lab1.grid(row=0)

lab2 = ttk.Label(window, text="Gravity")
lab2.grid(row=1,column=0)

value = tk.StringVar()
value.set("1.")

entry = ttk.Entry(window, textvariable=value, validate="key", validatecommand=(window.register(validate), "%P"))
entry.grid(row=1,column=1)

lab3 = ttk.Label(window, text="Scaling Ratio")
lab3.grid(row=1,column=2)

value1 = tk.StringVar()
value1.set("5.")

entry1 = ttk.Entry(window, textvariable=value1, validate="key", validatecommand=(window.register(validate), "%P"))
entry1.grid(row=1,column=3)



    
button = tk.Button(window,text="Ouvrir fichier", command=lambda:open_file())
button.grid(row=2)

# Create a Label
label1 = ttk.Label(window, text="Nombre d'itérations à appliquer fa2 \nen plus des 50 initiaux:")
label1.grid(row=3, column=0)

# Create a Combobox
combo1 = ttk.Combobox(window, values=[0, 50, 100, 500, 1000])
combo1.current(0)  # set the selected item
combo1.grid(row=3,column=1)

# Create a Label
label2 = ttk.Label(window, text="id du groupe:")
label2.grid(row=4, column=0)

# Create a Combobox pour choisir l'idée du groupe que l'on souhaite modifier 
#comms = community_louvain.best_partition(G)
#num_groups = len(set(comms.values()))
combo2 = ttk.Combobox(window, values=[i for i in range(1)])
combo2.current(0)  # set the selected item
combo2.grid(row=4,column=1)

# Create a Label
label3 = ttk.Label(window, text="Forme:")
label3.grid(row=3, column=2)

# Create a Combobox pour choisir l'idée du groupe que l'on souhaite modifier 
#comms = community_louvain.best_partition(G)
#num_groups = len(set(comms.values()))
combo3 = ttk.Combobox(window, values=['o','s','^','v','>','<','d','p','h','8','.','+','X'])
combo3.current(0)  # set the selected item
combo3.grid(row=3,column=3)

# Create a Label
label4 = ttk.Label(window, text="couleur:")
label4.grid(row=4, column=2)

# Create a Combobox pour choisir l'idée du groupe que l'on souhaite modifier 
#comms = community_louvain.best_partition(G)
#num_groups = len(set(comms.values()))
combo4 = ttk.Combobox(window, values=['black','red','blue','grey'])
combo4.current(0)  # set the selected item
combo4.grid(row=4,column=3)

button = tk.Button(window,text="generer graphe", command=lambda:dessiner_graphe())
button.grid(row=5)

labelSVG = ttk.Label(window, text="si vous souhaiter sauvegarder la dernière version  au format svg sellectionner le nom du fichier:")
labelSVG.grid(row=6,column=0)
entrySVG = ttk.Entry(window, validatecommand=(window.register(validate), "%P"))
entrySVG.grid(row=6,column=1)
buttonSVG = tk.Button(window,text="sauvegarde SVG", command=lambda:SaveSVG())
buttonSVG.grid(row=7)

button 
# Affichez la fenêtre
window.mainloop()

