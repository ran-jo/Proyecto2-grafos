import networkx as nx

#------------------------Variables------------------------#

ciudades = []
grafo = nx.Graph()

#------------------------Funciones------------------------#

def input_loop(texto, evaluacion, invalido):
    while True:
        var = input(texto)
        if evaluacion(var):
            return var
        else:
            print(invalido)


def calculo_peso(carretera, clima, bloqueo, delincuencia):
    return float(carretera)*0.2 + float(clima)*0.15 + float(delincuencia)*0.25 + (0.1*pow(float(bloqueo), 2) + 0.3)

#------------------------Ejecucion------------------------#

#       Ciudades

print("Ingrese el nombre de las ciudades a evaluar:")

while True:
    ciudades.append(input_loop("\tCiudad: ", lambda x: True if len(x.strip()) > 0 else False, "\t Ingrese un nombre valido"))

    if len(ciudades) > 2:
        cont = input("Ingrese \"S\" si desea agregar otra ciudad: ")
        if cont != "S": break


grafo.add_nodes_from(ciudades)
print(" ->", grafo.number_of_nodes(), "ciudades")


#       Conexiones

print("\nDe las ciudades")

for i in range(len(ciudades)):
    print("  ", i + 1, ":", ciudades[i])

print("Defina cada conexion y su estado:")

while True:
    node1 = input_loop("\tConexion de ciudad (Numero): ", lambda x: True if x in map(lambda y: str(y), range(1, len(ciudades) + 1)) else False, "\t  Ingrese una ciudad valida")
    node2 = input_loop("\tcon ciudad (Numero): ", lambda x: True if x in map(lambda y: str(y), range(1, len(ciudades) + 1)) else False, "\t  Ingrese una ciudad valida")

    if node1 == node2:
        print("Conexion no valida")
        print()
        continue

    print(f"  Evalue de 1 (poco) a 5 (mucho) la conexion entre {ciudades[int(node1) - 1]} y {ciudades[int(node2) - 1]}:")
    punt = []
    punt.append(input_loop("\t   Malestado de carretera: ", lambda x: True if x in map(lambda y: str(y), range(1, 6)) else False, "\t    Ingrese una numero valido"))
    punt.append(input_loop("\t   Mal clima: ", lambda x: True if x in map(lambda y: str(y), range(1, 6)) else False, "\t    Ingrese una numero valido"))
    punt.append(input_loop("\t   Bloqueos: ", lambda x: True if x in map(lambda y: str(y), range(1, 6)) else False, "\t    Ingrese una numero valido"))
    punt.append(input_loop("\t   Delincuencia: ", lambda x: True if x in map(lambda y: str(y), range(1, 6)) else False, "\t    Ingrese una numero valido"))

    peso = calculo_peso(punt[0], punt[1], punt[2], punt[3])
    grafo.add_edge(ciudades[int(node1) - 1], ciudades[int(node2) - 1], weight = peso)

    edge = [(u, v, w) for (u, v, w) in grafo.edges.data('weight')][-1]
    print(f" Conexion de {edge[0]} y {edge[1]} con peso de {edge[2]:0.3}")
    edge = [(u, v, w) for (u, v, w) in grafo.edges.data('weight')][0]
    print(f" Conexion de {edge[0]} y {edge[1]} con peso de {edge[2]:0.3}")
    print(f" Conexion de {ciudades[int(node1) - 1]} y {ciudades[int(node2) - 1]} con peso de {peso:0.3}")
    print()
    
    
    if grafo.number_of_edges() > 2:
        cont = input("Ingrese \"S\" si desea agregar otra conexion: ")
        if cont != "S": break


print(" ->", grafo.number_of_edges(), "conexiones")



#------------------------Algoritmo------------------------#


print("\n")

#       Centro de grafo (punto extra)

fw_paths = {c: dict(m) for c, m in nx.floyd_warshall(grafo).items()}
fw_eccen = {c: max( {v:k for k, v in fw_paths[c].items()} ) for c in fw_paths}
min_eccen = min(fw_eccen.values())
center = [c for c in fw_eccen if fw_eccen[c] == min_eccen]

print("-> El centro del grafo se encuentra en la ciudad(es)", ", ".join(center), "con eccentricidad de", min_eccen)

print()

while True:
    print("\nDe las ciudades")

    for i in range(len(ciudades)):
        print(" \t", i + 1, ":", ciudades[i])
    
    node1 = input_loop("  calcular ruta mas corta de ciudad (Numero): ", lambda x: True if x in map(lambda y: str(y), range(1, len(ciudades) + 1)) else False, "   Ingrese una ciudad valida")
    node2 = input_loop("  con ciudad (Numero): ", lambda x: True if x in map(lambda y: str(y), range(1, len(ciudades) + 1)) else False, "   Ingrese una ciudad valida")

    if node1 == node2:
        print("   Conexion no valida")
        print()
        continue

    algoritmo = int(input_loop("   Desea utilizar Dijkstra (1) o Bellman-Ford (2)?: ", lambda x: True if x == "1" or x == "2" else False, "    Ingrese el algoritmo a utilizar"))

    #         Bellman-Ford                o              Dijkstra
    func = nx.bellman_ford_path if algoritmo - 1 else nx.dijkstra_path

    path = func(grafo, ciudades[int(node1) - 1], ciudades[int(node2) - 1])

    ruta = "\nRuta de "
    for i in path:
        ruta += i + " a "
    
    ruta = ruta.removesuffix(" a ") + ", con peso de " + str(nx.path_weight(grafo, path, "weight"))
    print(ruta)


    cont = input("\nIngrese \"S\" si desea calcular otra ruta: ")
    if cont != "S": break

    


print("Feliz dia :D")

