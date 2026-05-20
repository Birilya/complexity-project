''' 
За основу реализации данного алгоритма была взята лекция прошлого года
Алгоритмы и структуры данных (продвинутый поток) 4. Алгоритм Штор-Вагнера. Дерево Гомори-Ху 
https://youtu.be/L8Cso3oEOUA?si=t7KPpQAVBTBjSc2d
'''

from collections import deque
from typing import List, Tuple, Set

# Используемые типы
Graph = List[List[int]] # матрица смежности графа с пропускными способностями
AdjList = List[List[int]] # лист смежности


def build_adj(G: Graph) -> AdjList:
    """Строит список смежности по матрице пропускных способностей.
    
    Аргументы:
        G: матрица n x n, G[u][v] > 0 если есть ребро u -> v.
    
    Возвращает:
        adj: adj[u] — список вершин v, куда есть ребро из u + обратные ребра
    """
    n = len(G)
    adj = [[] for _ in range(n)]
    for u in range(n):
        for v in range(n):
            if G[u][v] > 0 or G[v][u] > 0:
                adj[u].append(v)
    return adj


def min_cut(G: Graph, adj: AdjList, s: int, t: int) -> Tuple[int, List[bool]]:
    """Находит минимальный разрез между s и t алгоритмом Эдмондса-Карпа.
    
    Аргументы:
        G: матрица пропускных способностей.
        adj: список смежности для G.
        s, t: исток и сток.
    
    Возвращает:
        (flow, visited): величина максимального потока и маска вершин,
                         достижимых из s в остаточной сети.
    """
    result = 0
    cf = [row[:] for row in G]
    while True:
        flow = BFS(cf, adj, s, t)
        if flow == 0:
            break
        result += flow
    
    visited = get_reachable(cf, adj, s)
    return result, visited


def BFS(cf: Graph, adj: AdjList, s: int, t: int) -> int:
    """Ищет кратчайший увеличивающий путь в остаточной сети с помощью BFS алгоритма.
    
    Аргументы:
        cf: остаточная сеть (матрица пропускных способностей).
        adj: список смежности.
        s, t: исток и сток.
    
    Возвращает:
        Величина увеличивающего пути (0 если пути нет).
    """
    n = len(adj)
    parent = [-1] * n
    parent[s] = s
    queue = deque()
    queue.append(s)

    while queue and parent[t] == -1:
        u = queue.popleft()
        for v in adj[u]:
            if cf[u][v] > 0 and parent[v] == -1:
                parent[v] = u
                queue.append(v)
    
    if parent[t] == -1:
        return 0
    
    v = t
    max_flow = float('inf')
    while v != s:
        max_flow = min(cf[parent[v]][v], max_flow)
        v = parent[v]

    v = t
    while v != s:
        cf[parent[v]][v] -= max_flow
        cf[v][parent[v]] += max_flow
        v = parent[v]
    
    return max_flow


def get_reachable(cf: Graph, adj: AdjList, s: int) -> List[bool]:
    """Находит вершины, достижимые из s в остаточной сети.
    
    Аргументы:
        cf: остаточная сеть.
        adj: список смежности.
        s: стартовая вершина.
    
    Возвращает:
        visited: visited[v] == True если v достижима из s.
    """
    n = len(cf)
    visited = [False] * n
    queue = deque()
    queue.append(s)
    visited[s] = True

    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if cf[u][v] > 0 and not visited[v]:
                visited[v] = True
                queue.append(v)
    return visited


def get_cut_edges(adj: AdjList, visited: List[bool]) -> List[Tuple[int, int]]:
    """По visited находит рёбра минимального разреза.
    
    Аргументы:
        adj: список смежности.
        visited: маска вершин одной стороны разреза.
    
    Возвращает:
        Список рёбер (u, v), пересекающих разрез (u на стороне visited, v — нет).
    """
    cut_edges = []
    for u in range(len(visited)):
        if visited[u]:
            for v in adj[u]:
                if not visited[v]:
                    cut_edges.append((u, v))
    return cut_edges


def GomoryHu(G: Graph, adj: AdjList) -> List[Tuple[int, List[Tuple[int, int]]]]:
    """Строит дерево Гомори-Ху и возвращает список всех найденных разрезов.
    
    Аргументы:
        G: матрица пропускных способностей.
        adj: список смежности.
    
    Возвращает:
        cuts: список кортежей (weight, edges), где weight — вес разреза,
              edges — список рёбер этого разреза.
    """
    n = len(G)
    parent = [0] * n
    cuts = []        

    for s in range(1, n):
        t = parent[s]
        flow, visited = min_cut(G, adj, s, t)
        cuts.append((flow, get_cut_edges(adj, visited)))
        parent[s] = s
        for i in range(n):
            if parent[i] == t and visited[i]:
                parent[i] = s
    return cuts


def get_comps(adj: AdjList, removed_edges: Set[Tuple[int, int]]) -> int:
    """Считает количество компонент связности после удаления рёбер.
    
    Аргументы:
        adj: список смежности исходного графа.
        removed_edges: множество удалённых рёбер (u, v), где u < v.
    
    Возвращает:
        Количество компонент связности.
    """
    n = len(adj)
    visited = [False] * n
    comps = 0

    for i in range(n):
        if visited[i]:
            continue
        comps += 1
        visited[i] = True
        queue = deque()
        queue.append(i)
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                edge = (u, v) if u < v else (v, u)
                if edge not in removed_edges and not visited[v]:
                    visited[v] = True
                    queue.append(v)
    return comps


def EFFICIENT(G: Graph, k: int) -> Tuple[int, Set[Tuple[int, int]]]:
    """Алгоритм EFFICIENT для приближённого min k-cut.
    
    Аргументы:
        G: матрица пропускных способностей.
        k: требуемое число компонент.
    
    Возвращает:
        (total_weight, removed_edges): суммарный вес удалённых рёбер и
                                        множество удалённых рёбер.
    """
    n = len(G)
    adj = build_adj(G)

    cuts = GomoryHu(G, adj)
    cuts.sort(key=lambda x: x[0])
    
    union: Set[Tuple[int, int]] = set()
    for weight, cut_edges in cuts:
        for u, v in cut_edges:
            union.add((u, v) if u < v else (v, u))
        if get_comps(adj, union) >= k:
            break
    
    total_weight = sum(G[u][v] for u, v in union)
    return total_weight