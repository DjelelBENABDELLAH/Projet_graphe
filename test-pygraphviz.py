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
from forceatlas2.fa2.forceatlas2 import ForceAtlas2 
from fa2 import ForceAtlas2 as FA2
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import pyvista as pv



# Créez la fenêtre principale
window = tk.Tk()
window.title("Visualisation de graphe")
positions = None
pos_3D = None
G = None
node_colors = None
node_sizes = None
node_shapes = None
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
    global pos_3D
    pos_3D = None
    global node_colors
    node_colors = None 
    global node_sizes 
    node_sizes = None
    global node_shapes
    node_shapes = None
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
        jitterTolerance=float(entryJT.get()),  # Tolerance
        barnesHutOptimize=True,
        barnesHutTheta=float(entryBH.get()),
        multiThreaded=False,  # NOT IMPLEMENTED

        # Tuning
        scalingRatio=float(entry1.get()),
        strongGravityMode=False,
        gravity=float(entry.get()),

        # Log
        verbose=True) 

    pos_3D = forceatlas2.forceatlas2_networkx_layout(G, pos=pos_3D, iterations=3)
    
    forceatlas2 = FA2(
        # Behavior alternatives
        outboundAttractionDistribution=True,  # Dissuade hubs
        linLogMode=False,  # NOT IMPLEMENTED
        adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
        edgeWeightInfluence=1.0,

        # Performance
        jitterTolerance=float(entryJT.get()),  # Tolerance
        barnesHutOptimize=True,
        barnesHutTheta=float(entryBH.get()),
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
    
    # recréation du bouton en intégrant le bon nombre de groupe 
    global combo2
    combo2 = ttk.Combobox(window, values=[i for i in range(len(unique_coms))])
    combo2.current(0)  # set the selected item
    combo2.grid(row=6,column=1)
    
    
    # liste des couleurs que peuvent prendre les noeuds
    cmap = {
        0: 'red',
        1: 'teal',
        2: 'yellow',
        3: 'purple',
        4: 'orange',
        5: 'black',
        6: 'blue'
    }

    # choix de couleurs des noeuds selon l'id de leur groupe
    node_colors = [cmap[v % 7] for _, v in comms.items()]

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


    # Récupérez les degrés de tous les noeuds
    degrees = dict(G.degree())

    # Définissez la taille des noeuds en fonction de leur degré
    node_sizes = [(v * float(entryTaille.get())+5) for v in degrees.values()]


def dessiner_graphe_avec_forme_plus_lent():
    global positions 
    global node_colors
    global node_sizes
    global node_shapes
    global comms
    global G

    if(G == None):
        return Exception

     # Récupérez les degrés de tous les noeuds
    degrees = dict(G.degree())

    # Définissez la taille des noeuds en fonction de leur degré
    node_sizes = [(v * float(entryTaille.get())+5) for v in degrees.values()]

    forceatlas2 = FA2(
        # Behavior alternatives
        outboundAttractionDistribution=True,  # Dissuade hubs
        linLogMode=False,  # NOT IMPLEMENTED
        adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
        edgeWeightInfluence=1.0,

        # Performance
        jitterTolerance=float(entryJT.get()),  # Tolerance
        barnesHutOptimize=True,
        barnesHutTheta=float(entryBH.get()),
        multiThreaded=False,  # NOT IMPLEMENTED

        # Tuning
        scalingRatio=float(entry1.get()),
        strongGravityMode=False,
        gravity=float(entry.get()),

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
            node_shapes[i]=combo3.get()
        i=i+1
    #node_colors = [combo4.get() if ((v%7)==int(combo2.get())) else node_colors[int(i)] for i, v in comms.items()]
    #print(node_colors[1])
    #print(combo2.get())
    
    # création de la figure et du plot 2D
    # création de la figure et du plot 2D
    fig = plt.figure()
    ax = fig.add_subplot(111)

    i = 0
    # affichage des noeuds
    for node in G.nodes:
        x, y = positions[node]
        ax.scatter(x, y, c=node_colors[i], marker=node_shapes[i], s=node_sizes[i])
        i += 1

    # affichage des arêtes
    nx.draw_networkx_edges(G, positions, edge_color="black", alpha=1, style='dashed')


    # Masquez les axes
    plt.axis('off')

    # Enregistrer la figure au format SVG
    #plt.savefig("figure.svg")

    # Affichez la figure
    plt.show()



def dessiner_graphe_3D():
    global pos_3D
    global node_colors
    global node_sizes
    global node_shapes
    global comms
    global G

    if(G == None):
        return Exception

     # Récupérez les degrés de tous les noeuds
    degrees = dict(G.degree())

    # Définissez la taille des noeuds en fonction de leur degré
    node_sizes = [(v * float(entryTaille.get())+5) for v in degrees.values()]

    forceatlas2 = ForceAtlas2(
        # Behavior alternatives
        outboundAttractionDistribution=True,  # Dissuade hubs
        linLogMode=False,  # NOT IMPLEMENTED
        adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
        edgeWeightInfluence=1.0,

        # Performance
        jitterTolerance=float(entryJT.get()),  # Tolerance
        barnesHutOptimize=True,
        barnesHutTheta=float(entryBH.get()),
        multiThreaded=False,  # NOT IMPLEMENTED

        # Tuning
        scalingRatio=float(entry1.get()),
        strongGravityMode=False,
        gravity=float(entry.get()),

        # Log
        verbose=True)

    pos_3D = forceatlas2.forceatlas2_networkx_layout(G, pos=pos_3D, iterations=int(combo1.get()))
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
            node_shapes[i]=combo3.get()
        i=i+1
    
    # création de la figure et du plot 2D
    #fig = plt.figure()
    #ax = Axes3D(fig)

    #i = 0
    # affichage des noeuds
    #for node in G.nodes:
    #    x, y, z = positions[node]
    #    ax.scatter(x, y, z, c=node_colors[i], marker=node_shapes[i], s=node_sizes[i])
    #    i += 1
    # créer une figure et un axe 3D
    fig = plt.figure()
    ax = Axes3D(fig, auto_add_to_figure=False)
    fig.add_axes(ax)

    # dessiner les noeuds
    nodes = list(G.nodes)
    node_colors = np.array(node_colors)
    node_shapes = np.array(node_shapes)
    node_sizes = np.array(node_sizes)
    x, y, z = np.array([pos_3D[node] for node in nodes]).T
    ax.scatter(x, y, z, c=node_colors, marker=combo3.get(), s=node_sizes)

    # dessiner les arêtes
    edges = np.array([(pos_3D[edge[0]], pos_3D[edge[1]]) for edge in G.edges])
    edges = edges.reshape((-1, 3))
    x, y, z = edges.T
    ax.plot(x, y, z, c='black', linewidth=0.2)
    
    # affichage des arêtes
    #for edge in G.edges:
    #    x = [positions[edge[0]][0], positions[edge[1]][0]]
    #    y = [positions[edge[0]][1], positions[edge[1]][1]]
    #    z = [positions[edge[0]][2], positions[edge[1]][2]]
    #    ax.plot(x, y, z, c='black', linewidth=0.1)

    

    # Masquez les axes
    #plt.axis('off')

    # Enregistrer la figure au format SVG
    #plt.savefig("figure.svg")

    # Affichez la figure
    plt.show()

def dessiner_graphe():
    global positions
    global node_colors
    global node_sizes
    global node_shapes
    global comms
    global G

    if(G == None):
        return Exception

     # Récupérez les degrés de tous les noeuds
    degrees = dict(G.degree())

    # Définissez la taille des noeuds en fonction de leur degré
    node_sizes = [(v * float(entryTaille.get())+5) for v in degrees.values()]

    forceatlas2 = FA2(
        # Behavior alternatives
        outboundAttractionDistribution=True,  # Dissuade hubs
        linLogMode=False,  # NOT IMPLEMENTED
        adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
        edgeWeightInfluence=1.0,

        # Performance
        jitterTolerance=float(entryJT.get()),  # Tolerance
        barnesHutOptimize=True,
        barnesHutTheta=float(entryBH.get()),
        multiThreaded=False,  # NOT IMPLEMENTED

        # Tuning
        scalingRatio=float(entry1.get()),
        strongGravityMode=False,
        gravity=float(entry.get()),

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
            node_shapes[i]= combo3.get()
        i=i+1
    
    
    # Dessinez le graphe
    nx.draw_networkx_edges(G, positions, edge_color="black", alpha=1, style='dashed')
    nx.draw_networkx_nodes(G, positions, node_size=node_sizes, node_color=node_colors,node_shape= combo3.get(), alpha =0.8)
    
    # Masquez les axes
    plt.axis('off')

    # Affichez la figure
    plt.show()

def SaveSVG():
    
    # Dessinez le graphe
    nx.draw_networkx_edges(G, positions, edge_color="black", alpha=1, style='dashed')
    nx.draw_networkx_nodes(G, positions, node_size=node_sizes, node_color=node_colors,node_shape= combo3.get(), alpha =0.8)

    # Masquez les axes
    plt.axis('off')

    # Enregistrer la figure au format SVG
    plt.savefig(entrySVG.get())

def SaveSTL():
    
    #code non correcte il a donc était supprimer.

    print("sauvegarde SVG-3D terminer")

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

labBH = ttk.Label(window, text="BarnesHut")
labBH.grid(row=2,column=0)

valueBH = tk.StringVar()
valueBH.set("10.")

entryBH = ttk.Entry(window, textvariable=valueBH, validate="key", validatecommand=(window.register(validate), "%P"))
entryBH.grid(row=2,column=1)

labJT = ttk.Label(window, text="Jitter Tolerance")
labJT.grid(row=2,column=2)

valueJT = tk.StringVar()
valueJT.set("1.")

entryJT = ttk.Entry(window, textvariable=valueJT, validate="key", validatecommand=(window.register(validate), "%P"))
entryJT.grid(row=2,column=3)

labTaille = ttk.Label(window, text="Multiplicaeur taille du noeud en fonction de son degré")
labTaille.grid(row=3,column=0)

valueTaille = tk.StringVar()
valueTaille.set("0.5")

entryTaille = ttk.Entry(window, textvariable=valueTaille, validate="key", validatecommand=(window.register(validate), "%P"))
entryTaille.grid(row=3,column=1)



    
button = tk.Button(window,text="Ouvrir fichier", command=lambda:open_file())
button.grid(row=4)

# Create a Label
label1 = ttk.Label(window, text="Nombre d'itérations à appliquer fa2 \nen plus des 50 initiaux:")
label1.grid(row=5, column=0)

# Create a Combobox
combo1 = ttk.Combobox(window, values=[0, 50, 100, 500, 1000])
combo1.current(0)  # set the selected item
combo1.grid(row=5,column=1)

# Create a Label
label2 = ttk.Label(window, text="id du groupe:")
label2.grid(row=6, column=0)

# Create a Combobox pour choisir l'idée du groupe que l'on souhaite modifier 
#comms = community_louvain.best_partition(G)
#num_groups = len(set(comms.values()))
combo2 = ttk.Combobox(window, values=[i for i in range(1)])
combo2.current(0)  # set the selected item
combo2.grid(row=6,column=1)

# Create a Label
label3 = ttk.Label(window, text="Forme:")
label3.grid(row=6, column=2)

# Create a Combobox pour choisir l'idée du groupe que l'on souhaite modifier 
#comms = community_louvain.best_partition(G)
#num_groups = len(set(comms.values()))
combo3 = ttk.Combobox(window, values=['o','s','^','v','>','<','d','p','h','8','.','+','X'])
combo3.current(0)  # set the selected item
combo3.grid(row=5,column=3)

# Create a Label
label4 = ttk.Label(window, text="couleur:")
label4.grid(row=6, column=2)

# Create a Combobox pour choisir l'idée du groupe que l'on souhaite modifier 
#comms = community_louvain.best_partition(G)
#num_groups = len(set(comms.values()))
combo4 = ttk.Combobox(window, values=['black','red','blue','grey'])
combo4.current(0)  # set the selected item
combo4.grid(row=6,column=3)

button = tk.Button(window,text="generer graphe 3D", command=lambda:dessiner_graphe_3D())
button.grid(row=7, column=0)

button = tk.Button(window,text="generer graphe", command=lambda:dessiner_graphe())
button.grid(row=7, column=1)

button = tk.Button(window,text="generer graphe avec forme plus lent", command=lambda:dessiner_graphe_avec_forme_plus_lent())
button.grid(row=7, column=2)

labelSVG = ttk.Label(window, text="si vous souhaiter sauvegarder la dernière version  au format svg sellectionner le nom du fichier:")
labelSVG.grid(row=8,column=0)
entrySVG = ttk.Entry(window, validatecommand=(window.register(validate), "%P"))
entrySVG.grid(row=8,column=1)

buttonSVG = tk.Button(window,text="sauvegarde SVG", command=lambda:SaveSVG())
buttonSVG.grid(row=9,column=1)

#sauvegarde en stl qui c'est soldé que par des erreus lors de la compilation ou des fichiers complétement vide
#buttonSTL = tk.Button(window,text="sauvegarde STL", command=lambda:SaveSTL())
#buttonSTL.grid(row=9,column=2)


# Affichez la fenêtre
window.mainloop()

