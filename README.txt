Introduction :
Notre application de visualisation de grands graphes est une solution pratique pour visualiser des graphes massifs de manière efficace. Avec cette application, 
les utilisateurs peuvent visualiser les graphes de manière interactive et exploratoire. Ce README est conçu pour vous aider à comprendre comment 
utiliser l'application de visualisation de grands graphes.

Prérequis :
Avant d'utiliser notre implémentation, il est nécessaire que Python soit installé sur votre machine. Pour exécuter le script, 
vous devez avoir les librairies utilisées avec leurs bonnes versions. 

ATTENTION : Nous avons dans lors de notre projet utilisée la version 3.10.9 de python. il se peut que la version des librairie doivent être différente pour une autre version.

il vous faudra tout d'abord installer tkinter, vous pouvez utiliser la commande suivante selon votre système d'exploitation :
Sur Ubuntu/Debian : sudo apt-get install python3-tk
Sur MacOS : tkinter est pré-installé avec Python
Sur Windows : tkinter est pré-installé avec Python

Ensuite installer la liste de librairie suivante
- pygraphviz avec la commande pip depuis votre terminal: pip install pygraphviz==1.10

- community avec la commande pip depuis votre terminal: pip install python-louvain==0.16

- networkx avec la commande pip depuis votre terminal: pip install networkx==2.5

- numpy avec la commande pip depuis votre terminal: pip install numpy==1.24.1

- matplotlib avec la commande pip depuis votre terminal: pip install matplotlib==3.5.1

- forceatlas2 avec la commande pip depuis votre terminal: pip install fa2==0.3.5

- mpl_toolkits avec la commande pip depuis votre terminal: pip install mplot3d

Enfin il faudra récupéré le dossier fa2 présent sur le git pour la partie 3D et le situé au même niveau que l'executable.


Utilisation :
Une fois que vous avez vérifié que Python est installé sur votre machine et que vous avez les librairies requises, 
vous pouvez exécuter notre script principal pour utiliser l'API de visualisation de grands graphes.

Pour commencer, vous devez importer les données du graphe que vous souhaitez visualiser. 
Les données du graphe doivent être dans un format compatible avec notre API '.dot'. Ensuite, vous pouvez lancer le script principal 
pour afficher le graphe à l'aide de la commande suivante :

python main.py

Cela va lancer l'application et vous permettre d'interagir avec le graphe.

Pour plus de détaille concernant les possibilités je vous redirige vers la vidéo.

Conclusion :
Notre application de visualisation de grands graphes est une solution pratique pour visualiser les graphes massifs de manière efficace. 
Avec cette application, les utilisateurs peuvent visualiser les graphes de manière interactive et exploratoire. 
Nous espérons que cette documentation vous a aidé à comprendre comment utiliser l'application de visualisation de grands graphes. 
Si vous avez des questions ou des commentaires, n'hésitez pas à nous contacter.

