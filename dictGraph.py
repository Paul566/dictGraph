from wordfreq import top_n_list
import numpy as np
import matplotlib.pyplot as plt
import json


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def areAdjacent(s1, s2):
    if abs(len(s1) - len(s2)) >= 2:
        return False

    if len(s1) == len(s2):
        dif = 0
        for i in range(len(s1)):
            if s1[i] != s2[i]:
                dif += 1
            if dif == 2:
                return False
        if dif == 1:
            return True
        else:
            return False

    if len(s1) < len(s2):
        aux = s1
        s1 = s2
        s2 = aux
    cur = 0
    while (s1[cur] == s2[cur]):
        cur += 1
        if cur == len(s2):
            break
    for i in range(cur, len(s2)):
        if s1[i + 1] != s2[i]:
            return False
    return True


def saveEdges(words, filename):
    print('Creating the list of edges...')
    n = len(words)
    edges = set()
    for i in range(n):
        printProgressBar(2 * i * (n - i) + i * i + 1, n * n)
        for j in range(i + 1, n):
            if areAdjacent(words[i], words[j]):
                edges.add((i, j))
    with open(filename + '.json', 'w') as f:
        json.dump(list(edges), f)


def plotSpectrum(file_read, file_write, n, label):
    vals = []
    f = open(file_read, 'r')
    for i in range(n):
        vals.append(float(f.readline()))
    plt.figure()
    plt.yticks([])
    plt.title(label)
    plt.hist(vals, density=True, bins=round(np.sqrt(n)))
    plt.savefig(file_write + '.png', dpi=200)


def plotCompData(file_read, file_write, label, n):
    sizes = []
    counts = []
    f = open(file_read, 'r')
    for i in range(n):
        fields = f.readline().split()
        sizes.append(int(fields[0]))
        counts.append(int(fields[1]))

    '''fig, ax = plt.subplots(1)
    plt.xlabel('размер компоненты связности')
    plt.ylabel('количество компонент связности данного размера')
    plt.title(label)
    plt.xlim(0.8, 50)
    plt.yscale('log')
    plt.xscale('log')
    ax.scatter(sizes, counts, marker='o')
    plt.savefig(file_write + '.png', dpi=200)'''


def printLongestPath(words, filename, n):
    f = open(filename, 'r')
    for i in range(n):
        print(words[int(f.readline())])


if __name__ == "__main__":
    n = 20000
    #print(top_n_list('en', 50, wordlist='best'))
    #words_en = top_n_list('en', n, wordlist='best')
    #words_ru = top_n_list('ru', n, wordlist='best')
    #saveEdges(words_en, 'edges_en_10')
    #saveEdges(words_ru, 'edges_ru')

    #plotSpectrum('spectrum_ru_20k', 'spectrum_ru_20k', n, 'Russian')
    plotCompData('componentsData_en_20k', 'componentsData_en_20k_loglog', 'English', n=27)
    #printLongestPath(words_ru, 'longestPath_ru_20k', n=31)
