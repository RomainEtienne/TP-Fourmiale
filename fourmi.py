import math
import pants
import csv
import networkx as nx
import matplotlib.pyplot as plt

#Calcul de la variance a partir d'une liste
def variance(liste): 
    print("Liste Variance ", liste)
    return moyenne([x**2 for x in liste]) - moyenne(liste)**2

#Calcul de la moyenne a partir d'une liste
def moyenne(liste): 
    print("Liste ",liste)
    return sum(liste) / len(liste)



G=nx.Graph()
nbBoucle=2
#Nombre d'élements de notre population
nbElement = 30

noeuds = []
#Création des noeuds à partir du csv(Easting/Northing)
with open('open_pubs.csv', 'r') as csvfile:
    rows = csv.reader(csvfile, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL)
    for row in rows:
        try:
            easting = float(row[4])
            northing = float(row[5])
            noeuds.append((easting, northing))
        except:
            continue

#Calcul de la distance a partir de Easting/Northing
def distance(a, b):
    eastingA = a[0] 
    northingA = a[1]
    eastingB = b[0] 
    northingB = b[1]
    eastingTotal = abs(eastingA - eastingB)
    northingTotal = abs(northingA - northingB)
	 #6 Digit donc resultat en metre
    d = math.sqrt(math.pow(eastingTotal,2) + math.pow(northingTotal,2))
    return d;

listeDistance = [];
#Boucle pour obtenir le nombre de solution souhaité
for i in range(nbBoucle):
    pop = noeuds[i*nbElement:(i+1)*nbElement]
    #Suppression des doublons
    pop = set(pop)
    pop = list(pop)
    
    G.clear()
    #Calcul de la solution
    monde = pants.World(pop, distance)
    solver = pants.Solver()
    solution = solver.solve(monde)
    print("Distance ", solution.distance)
    listeDistance.append(solution.distance);
    print("Tour ", solution.tour)
    #Ajout au graph
    for edge in solution.path:
        G.add_edge(edge.start, edge.end)
    #G.add_edges_from(solution.tour)
    plt.clf()
    nx.draw(G)
    plt.pause(1)
    
    #Enregistrement du fichier dans le dossier graph qui se trouve au même endroit que ce fichier
    plt.title("distance = %s" % solution.distance)
    plt.savefig("./graph/g_%s.png" % i, bbox_inches="tight")
    plt.show()


print("Moyenne ", moyenne(listeDistance))
print("Variance ", variance(listeDistance))
    

