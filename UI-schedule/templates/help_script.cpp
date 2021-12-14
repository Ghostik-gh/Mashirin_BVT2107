#include <bits/stdc++.h>

using namespace std;

int main(){
	setlocale(LC_ALL,"Russian");
    ifstream fin ("teachers.txt");
    ofstream fout("ex.txt");
    string str;
    for (int i = 0; i < 17; ++i){
    	fout << "INSERT INTO teachers (id, full_name, fk_subject) VALUES (";
    	for(int j = 0; j < 5; ++j){
    		fin >> str;
    		if(j == 1 or j == 4) fout << ",";
			if(j == 2 or j == 3) fout << " ";
    		for(int g = 0; g < str.size(); ++g){
    			if (str[g] == '"')
    				fout << "'";
    			else
    				fout << str[g];
			}
		}
		fout << ");\n";
	}
}
