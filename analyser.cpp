#include <iostream>
#include "json.hpp"
#include <fstream>
#include "string"
#include "vector"
#include "unordered_map"
#include "unordered_set"
#include "queue"
#include <Eigen/Core>
#include <Eigen/SparseCore>
#include <Eigen/Eigenvalues>
#include <iomanip>

using json = nlohmann::json;

class MyHash {
public:
    std::size_t operator()(const std::pair<int, int> &p) const {
        return std::hash<int>()(p.first) ^ std::hash<int>()(p.second);
    }
};

std::vector<std::pair<int, int>> readEdges(std::string filename) {
    std::cout << "reading edges...\n";
    json input;
    std::ifstream edgesFile(filename, std::ifstream::binary);
    edgesFile >> input;
    std::vector<std::pair<int, int>> edges = input.get<std::vector<std::pair<int, int>>>();
    return edges;
}

std::vector<std::vector<int>> getAdjList(std::vector<std::pair<int, int>> edges, int n) {
    std::cout << "creating AdjList...\n";
    std::vector<std::vector<int>> a;
    for (int i = 0; i < n; i++) {
        a.push_back(std::vector<int>());
    }
    for (auto e: edges) {
        a[e.first].push_back(e.second);
        a[e.second].push_back(e.first);
    }
    return a;
}

void writeSpectrum(std::vector<std::pair<int, std::vector<int>>> adjList, std::string filename) {
    int n = adjList.size();
    if (n == 1) {
        std::ofstream output;
        output.open(filename, std::ios_base::app);
        output << "1\n";
        output.close();
        return;
    }
    if (n == 2) {
        std::ofstream output;
        output.open(filename, std::ios_base::app);
        output << "0\n2\n";
        output.close();
        return;
    }
    if (n == 3) {
        std::ofstream output;
        output.open(filename, std::ios_base::app);
        if (adjList[0].second.size() + adjList[1].second.size() + adjList[2].second.size() == 4)
            output << "0\n1\n2\n";
        else
            output << "0\n1.5\n1.5\n";
        output.close();
        return;
    }
    if (n >= 100)
        std::cout << "component of size " << n << '\n';
    std::unordered_map<int, int> dict;
    for (int i = 0; i < n; i++) {
        dict.insert({adjList[i].first, i});
    }

    Eigen::SparseMatrix<float> L(n, n);
    L.reserve(
            Eigen::VectorXi::Constant(L.cols(), 100)); //100 is almost surely twice greater than degree of a given node
    for (int i = 0; i < n; i++) {
        L.insert(i, i) = 1;
        for (int to: adjList[i].second) {
            L.insert(i, dict[to]) = -1.0 / sqrt(adjList[i].second.size() * adjList[dict[to]].second.size());
        }
    }
    Eigen::SelfAdjointEigenSolver <Eigen::MatrixXf> es(n);
    es.Eigen::SelfAdjointEigenSolver<Eigen::MatrixXf>::compute(L, 0x40);

    std::ofstream output;
    output.open(filename, std::ios_base::app);
    output << es.Eigen::SelfAdjointEigenSolver<Eigen::MatrixXf>::eigenvalues();
    output << '\n';
    output.close();
}

void writeCompData(std::vector<std::vector<std::pair<int, std::vector<int>>>> compAdjList, std::string filename) {
    std::unordered_map<int, int> data;
    for (auto c: compAdjList) {
        if (data.find(c.size()) == data.end())
            data.insert({c.size(), 1});
        else
            data[c.size()]++;
    }
    std::ofstream output;
    output.open(filename);
    for (auto p: data)
        output << p.first << ' ' << p.second << '\n';
    output.close();
}

void getComponent(std::vector<std::vector<int>> adjList, int root, std::unordered_set<int> &visited) {
    visited.insert(root);
    for (int to: adjList[root]) {
        if (visited.find(to) == visited.end())
            getComponent(adjList, to, visited);
    }
}

std::vector<std::vector<std::pair<int, std::vector<int>>>> componentize(std::vector<std::vector<int>> adjList) {
    std::cout << "starting componentization...\n";
    std::vector<std::vector<std::pair<int, std::vector<int>>>> compAdjLists;
    int n = adjList.size();
    std::unordered_set<int> unvisited;
    for (int i = 0; i < n; i++)
        unvisited.insert(i);
    while (unvisited.size()) {
        std::vector<std::pair<int, std::vector<int>>> curAdjList;
        int root = *unvisited.begin();
        std::unordered_set<int> newlyVisited;
        getComponent(adjList, root, newlyVisited);
        for (int i: newlyVisited) {
            curAdjList.push_back(std::pair<int, std::vector<int>>(i, adjList[i]));
            unvisited.erase(i);
        }
        compAdjLists.push_back(curAdjList);
    }
    return compAdjLists;
}

void writeLongestPath(std::vector<std::vector<int>> adjList, std::string filename) {
    int maxdist = 0;
    int from, to;
    int n = adjList.size();
    for (int i = 0; i < n; i++) {
        std::queue<int> q;
        q.push(i);
        std::vector<int> dist(n, INT32_MAX);
        dist[i] = 0;
        while (!q.empty()) {
            int cur = q.front();
            q.pop();
            for (auto v: adjList[cur]) {
                if (dist[v] != INT32_MAX)
                    continue;
                dist[v] = dist[cur] + 1;
                q.push(v);
            }
        }
        for (int j = 0; j < n; j++) {
            if ((dist[j] < INT32_MAX) && (maxdist < dist[j])) {
                maxdist = dist[j];
                from = i;
                to = j;
            }
        }
    }

    std::cout << "maximal distance found: " << maxdist << '\n';

    std::queue<int> q;
    q.push(from);
    std::vector<int> dist(n, INT32_MAX);
    dist[from] = 0;
    while (!q.empty()) {
        int cur = q.front();
        q.pop();
        for (auto v: adjList[cur]) {
            if (dist[v] != INT32_MAX)
                continue;
            dist[v] = dist[cur] + 1;
            q.push(v);
        }
    }

    std::ofstream output;
    output.open(filename);
    int cur = to;
    while(dist[cur] > 0) {
        output << cur << '\n';
        for (int candidate : adjList[cur]) {
            if (dist[candidate] == dist[cur] - 1) {
                cur = candidate;
                break;
            }
        }
    }
    output << from;
    output.close();
}

int main() {
    std::cout.precision(12);
    int n = 20000;
    auto edges = readEdges("edges_ru_20k.json");
    auto adjList = getAdjList(edges, n);
    std::cout << n << " nodes\n";
    std::cout << edges.size() << " edges\n";
    //auto compAdjList = componentize(adjList);
    //for (auto adj: compAdjList)
    //    writeSpectrum(adj, "spectrum_ru_20k");
    //writeCompData(compAdjList, "componentsData_ru_20k");
    //writeLongestPath(adjList, "longestPath_ru_20k");
    return 0;
}
