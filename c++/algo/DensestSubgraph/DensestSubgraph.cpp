// DensestSubgraph.cpp : Ce fichier contient la fonction 'main'. L'exécution du programme commence et se termine à cet endroit.
//

#include <iostream>
#include <vector> 
#include <fstream>
#include <sstream>
#include <string>
#include <algorithm>
#include <chrono>
#include <filesystem>

using namespace std;
namespace fs = std::filesystem;//C++17 only


bool endsWith(const std::string& mainStr, const std::string& toMatch)
{
    if (mainStr.size() >= toMatch.size() &&
        mainStr.compare(mainStr.size() - toMatch.size(), toMatch.size(), toMatch) == 0)
        return true;
    else
        return false;
}
vector<pair<int, int>> read_file(string path) {
    vector<pair<int, int>> vertices;
    if (endsWith(path,"txt")) {
        std::ifstream infile(path);
        int a, b;
        while (infile >> a >> b)
        {
            if (a != b) {
                vertices.push_back(std::make_pair(a, b));
            }
            // else{
            //     self_loops.push_back(a);
            // }

        }
    }
    else {
        ifstream infile(path);
        string line;
        string str;
        getline(infile, line);
        while (getline(infile, line))
        {
            istringstream ss(line);
            vector <string> record;
            (getline(ss, str, ','));
            int a = std::stoi(str);
            (getline(ss, str, ','));
            int b = std::stoi(str);
           
            if(a!=b) vertices.push_back(std::make_pair(a,b));
        }
    }
    
 

   
    //std::cout << "slefloop len : " << self_loops.size() << "\n";
    
    return vertices;
}
vector<int>* list_adjacence(vector<pair<int, int>> vertices, int nodes) {
    vector<int>* L = new vector<int>[nodes];
    for (int i = 0;i < vertices.size();i++) {
        (L + vertices[i].first)->push_back(vertices[i].second);
        (L + vertices[i].second)->push_back(vertices[i].first);
    }
    //std::cout << "L " << (*(L+2))[1]<< "\n";
    return L;
}

int* degree_function(vector<int>* adj, int nodes) {
    int* degrees = new int[nodes] {0};
    for (int i = 0;i < nodes;i++) {
        *(degrees + i) = (adj+i)->size();
    }
    return degrees;

}

vector<int>* list_nodes_by_degree(int* degrees,int nodes,int max_d) {
    
    vector<int>* L = new vector<int>[max_d+1];
    for (int i = 0;i < nodes;i++) {
      
        (L + (*(degrees+i)))->push_back(i);
    }
    return L;
}
void algo(string path) {
    auto t1 = std::chrono::high_resolution_clock::now();
    int nodes = 0;
    vector<pair<int, int>> vertices = read_file(path);
    
    for (int i = 0;i < vertices.size();i++) {
        nodes = max(max(vertices[i].first, vertices[i].second), nodes);
    }
    nodes++;
    vector<int>* adjacent = list_adjacence(vertices, nodes);
    int E = vertices.size();
    int V = nodes;
    vector<pair<int, int>>().swap(vertices);
    int* deg = degree_function(adjacent, nodes);

    int d_min = *deg;
    int d_max = 0;
    for (int i = 0;i < nodes;i++) {
        d_max = max(d_max, (*(deg + i)));
        d_min = min(d_min, (*(deg + i)));
    }

    vector<int>* L_degrees = list_nodes_by_degree(deg, nodes, d_max);
    bool* binary_removed = new bool[nodes] {false};
    int* removed = new int[nodes] {0};
    std::pair<int, int>* v_removed = new std::pair<int, int>[E];
    float p, d = (float)E / (float)V;
    int l = 0;
    int m = 0;
    int length_removed = 0;
    int  length_v_removed = 0;
    int my_node = 0;
    int card_v = V;
    int card_E = E;


    while (length_removed != nodes) {

        while (true) {

            while (d_min < d_max && (L_degrees + d_min)->size() == 0) {

                d_min++;
            }

            my_node = (L_degrees + d_min)->back();
            (L_degrees + d_min)->pop_back();

            if (*(binary_removed + my_node) == false) break;
        }

        *(removed + length_removed) = my_node;
        length_removed++;
        *(binary_removed + my_node) = true;
        float k = 0;

        for (int i = 0;i < (adjacent + my_node)->size();i++) {

            int voisin = (*(adjacent + my_node))[i];
            if (!(*(binary_removed + voisin))) {
                k++;
                (L_degrees + (*(deg + voisin)) - 1)->push_back(voisin);
                if ((*(deg + voisin)) == d_min) d_min--;
                (*(deg + voisin))--;
                *(v_removed + length_v_removed) = std::make_pair(voisin, my_node);
                length_v_removed++;
            }
        }

        V--;
        E -= k;
        if (V != 0 && ((float)E / (float)V) > d) {
            l = length_removed;
            m = length_v_removed;
            d = ((float)E / (float)V);

        }

    }


   
    delete[] removed;
    delete[] binary_removed;
    delete[] adjacent;
    delete[] deg;
    delete[] L_degrees;
    auto t2 = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(t2 - t1).count();
    std::cout <<"duration (sec) : "<< (float)duration/(float)1000000 << "\n";
    std::cout << "n and  m :" << card_v << "   " << card_E << "\n";
    std::cout << "density : " << d << "\n";
    
  
}
int main()
{
    for (const auto& entry : fs::directory_iterator("../../../graphs")) {
   
        std::cout << (entry.path()).u8string() << "\n";
        algo((entry.path()).u8string());

        std::cout << "======================" << "\n";
    }

    system("pause pressy key to exit");//windows only
    
}

//delete list adjacence


// Exécuter le programme : Ctrl+F5 ou menu Déboguer > Exécuter sans débogage
// Déboguer le programme : F5 ou menu Déboguer > Démarrer le débogage

// Astuces pour bien démarrer : 
//   1. Utilisez la fenêtre Explorateur de solutions pour ajouter des fichiers et les gérer.
//   2. Utilisez la fenêtre Team Explorer pour vous connecter au contrôle de code source.
//   3. Utilisez la fenêtre Sortie pour voir la sortie de la génération et d'autres messages.
//   4. Utilisez la fenêtre Liste d'erreurs pour voir les erreurs.
//   5. Accédez à Projet > Ajouter un nouvel élément pour créer des fichiers de code, ou à Projet > Ajouter un élément existant pour ajouter des fichiers de code existants au projet.
//   6. Pour rouvrir ce projet plus tard, accédez à Fichier > Ouvrir > Projet et sélectionnez le fichier .sln.
