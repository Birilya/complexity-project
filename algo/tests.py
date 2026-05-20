import networkx as nx
from itertools import product
import random
from algorithm import *
import time

def optimal_k_cut(G: Graph, k: int) -> int:
    """Точный минимальный k-разрез полным перебором. n <= 8."""
    n = len(G)
    best = float('inf')
    
    for assignment in product(range(k), repeat=n): # генерируем распределение на k компонент
        if len(set(assignment)) < k:
            continue
        
        weight = 0
        for u in range(n):
            for v in range(u + 1, n):
                if assignment[u] != assignment[v]:
                    weight += G[u][v]
        
        best = min(best, weight)
    return best

def test_efficient(G: Graph, k: int) -> dict:
    """Сравнивает EFFICIENT с оптимальным решением."""
    start1 = time.perf_counter()
    opt = optimal_k_cut(G, k)
    end1 = time.perf_counter()

    start2 = time.perf_counter()
    efficient = EFFICIENT(G, k)
    end2 = time.perf_counter()
    
    res = efficient / opt if opt > 0 else 1.0
    bound = 2 - 2 / k
    
    return {
        'optimal': opt,
        'efficient': efficient,
        'res': res,
        'bound': bound,
        'status': res <= bound + 1e-9,  # погрешность
        'opt_time': end1 - start1,
        'eff_time': end2 - start2,
    }

def read_graph(filepath):
    """Читает файл graph6 и возвращает список графов в виде матриц смежности."""
    graphs = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('>'):
                g = nx.from_graph6_bytes(line.encode())
                n = g.number_of_nodes()
                mat = [[0] * n for _ in range(n)]
                for u, v in g.edges():
                    mat[u][v] = 1
                    mat[v][u] = 1
                graphs.append(mat)
    return graphs

def vert_checker(test_count, subdir):
    for n, count in test_count.items():
        print(f"\n{'='*60}")
        print(f"\t\tn = {n}, вид тестов: {subdir}")
        print(f"{'='*60}")
        
        all_graphs = read_graph(f"./tests/vertices/{subdir}/{n}.txt")
        count = min(count, len(all_graphs))
        graphs = random.sample(all_graphs, count)
        
        for k in range(2, n + 1):
            res_data = []
            opt_time = []
            eff_time = []
            
            for g_idx, G in enumerate(graphs):
                review = test_efficient(G, k)
                res_data.append(review['res'])
                opt_time.append(review['opt_time'])
                eff_time.append(review['eff_time'])
                
                
                if not review['status']:
                    print(f"\n{'!'*60}")
                    print(f"Тест не пройден")
                    print(f"  n = {n}, k = {k}, граф №{g_idx}")
                    print(f"  Матрица смежности G:")
                    for row in G:
                        print(f"\t\t{row}")
                    print(f"\tОптимальный разрез (OPT): {review['optimal']}")
                    print(f"\tОтвет EFFICIENT:        {review['efficient']}")
                    print(f"\tОтношение EFF/OPT:      {round(review['res'], 8)}")
                    print(f"\tТеоретическая граница:  {round(review['bound'], 8)}")
                    print(f"{'!'*60}")
                    return
            print(f"Тест c k={k} пройдены")
            print(f"Количество тестов: {len(res_data)}")
            avg_res = sum(res_data) / len(res_data)
            max_res = max(res_data)
            min_res = min(res_data)
            avg_opt_time = sum(opt_time) / len(opt_time)
            avg_eff_time = sum(eff_time) / len(eff_time)
            
            
            print(f"\t Допустимое отношение eff/opt: {round(2 - 2/k, 10)}")
            print(f"\t Лучшее: {round(min_res, 10)}") 
            print(f"\t Худшее: {round(max_res, 10)}")
            print(f"\t В среднем: {round(avg_res, 10)}")
            print(f"\t Среднее время EFFICIENT: {round(avg_eff_time, 8)}s")
            print(f"\t Среднее время checker-а: {round(avg_opt_time, 8)}s\n")
    print(f"\n{'='*60}")
    print("Все тесты пройдены успешно!")

def edge_checker(test_count, subdir):
    for m, count in test_count.items():
        print(f"\n{'='*60}")
        print(f"\t\tm = {m}, вид тестов: {subdir}")
        print(f"{'='*60}")
        
        all_graphs = read_graph(f"./tests/edges/{subdir}/{m}.txt")
        count = min(count, len(all_graphs))
        graphs = random.sample(all_graphs, count)
        
        for k in range(2, m + 1):
            res_data = []
            opt_time = []
            eff_time = []
            
            for g_idx, G in enumerate(graphs):
                if (k + 1 > len(G)):
                    continue
                if len(G) > 8:  # optimal_k_cut слишком медленный для n > 8 ;(
                    continue
                review = test_efficient(G, k)
                res_data.append(review['res'])
                opt_time.append(review['opt_time'])
                eff_time.append(review['eff_time'])
                
                
                if not review['status']:
                    print(f"\n{'!'*60}")
                    print(f"Тест не пройден")
                    print(f"  m = {m}, k = {k}, граф №{g_idx}")
                    print(f"  Матрица смежности G:")
                    for row in G:
                        print(f"\t\t{row}")
                    print(f"\tОптимальный разрез (OPT): {review['optimal']}")
                    print(f"\tОтвет EFFICIENT:        {review['efficient']}")
                    print(f"\tОтношение EFF/OPT:      {round(review['res'], 8)}")
                    print(f"\tТеоретическая граница:  {round(review['bound'], 8)}")
                    print(f"{'!'*60}")
                    return
            print(f"Тест c k={k} пройдены")
            print(f"Количество тестов: {len(res_data)}")
            avg_res = sum(res_data) / len(res_data)
            max_res = max(res_data)
            min_res = min(res_data)
            avg_opt_time = sum(opt_time) / len(opt_time)
            avg_eff_time = sum(eff_time) / len(eff_time)
            
            
            print(f"\t Допустимое отношение eff/opt: {round(2 - 2/k, 10)}")
            print(f"\t Лучшее: {round(min_res, 10)}") 
            print(f"\t Худшее: {round(max_res, 10)}")
            print(f"\t В среднем: {round(avg_res, 10)}")
            print(f"\t Среднее время EFFICIENT: {round(avg_eff_time, 8)}s")
            print(f"\t Среднее время checker-а: {round(avg_opt_time, 8)}s\n")
    print(f"\n{'='*60}")
    print("Все тесты пройдены успешно!")


def generate_trees(max_n: int, test_count: dict) -> dict:
    """Генерирует случайные деревья для каждого n от 2 до max_n.
    
    Аргументы:
        max_n: максимальное число вершин.
        test_count: сколько деревьев сгенерировать для каждого n.
    
    Возвращает:
        Словарь {n: список матриц смежности}.
    """
    trees = {}
    for n in range(2, max_n + 1):
        trees[n] = []
        for _ in range(test_count[n]):
            t = nx.random_labeled_tree(n)
            mat = [[0] * n for _ in range(n)]
            for u, v in t.edges():
                mat[u][v] = 1
                mat[v][u] = 1
            trees[n].append(mat)
    return trees


def tree_checker(max_n, test_count):
    trees = generate_trees(max_n, test_count)
    
    for n, graphs in trees.items():
        print(f"\n{'='*60}")
        print(f"\t\tn = {n}, вид тестов: деревья")
        print(f"{'='*60}")
        
        for k in range(2, n + 1):
            res_data = []
            opt_time = []
            eff_time = []
            
            for g_idx, G in enumerate(graphs):
                review = test_efficient(G, k)
                res_data.append(review['res'])
                opt_time.append(review['opt_time'])
                eff_time.append(review['eff_time'])
                
                if not review['status']:
                    print(f"\n{'!'*60}")
                    print(f"Тест не пройден")
                    print(f"  n = {n}, k = {k}, дерево №{g_idx}")
                    print(f"  Матрица смежности G:")
                    for row in G:
                        print(f"\t\t{row}")
                    print(f"\tОптимальный разрез (OPT): {review['optimal']}")
                    print(f"\tОтвет EFFICIENT:        {review['efficient']}")
                    print(f"\tОтношение EFF/OPT:      {round(review['res'], 8)}")
                    print(f"\tТеоретическая граница:  {round(review['bound'], 8)}")
                    print(f"{'!'*60}")
                    return
            
            print(f"Тест c k={k} пройдены")
            print(f"Количество тестов: {len(res_data)}")
            avg_res = sum(res_data) / len(res_data)
            max_res = max(res_data)
            min_res = min(res_data)
            avg_opt_time = sum(opt_time) / len(opt_time)
            avg_eff_time = sum(eff_time) / len(eff_time)
            
            print(f"\t Допустимое отношение eff/opt: {round(2 - 2/k, 10)}")
            print(f"\t Лучшее: {round(min_res, 10)}")
            print(f"\t Худшее: {round(max_res, 10)}")
            print(f"\t В среднем: {round(avg_res, 10)}")
            print(f"\t Среднее время EFFICIENT: {round(avg_eff_time, 8)}s")
            print(f"\t Среднее время checker-а: {round(avg_opt_time, 8)}s\n")
    
    print(f"\n{'='*60}")
    print("Все тесты пройдены успешно!")



if __name__ == "__main__":
    # Можете выбрать количество тестов для каждого n
    vert_test_count = {
        2: 40,
        3: 40,
        4: 40,
        5: 40,
        6: 40,
        7: 30,
        8: 15,
        9: 5
    }

    edge_test_count = {
        2: 30,
        3: 30,
        4: 30,
        5: 30,
        6: 20,
        7: 20,
        8: 20,
        9: 10,
        10: 10,
        11: 10,
        12: 10,
        13: 10
    }

    # =========== Запуск тестов =============
    # vert_checker(vert_test_count, "all")
    # vert_checker(vert_test_count, "connected")

    edge_checker(edge_test_count, "all")
    edge_checker(edge_test_count, "connected")

    tree_checker(9, vert_test_count)
