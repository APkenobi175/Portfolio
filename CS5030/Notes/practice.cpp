#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>

int main(){
    int n = 15;
    int p = 3;

    // Total time on each core
    std::vector<int> time(p,0); // this creates a vector of size p with all 0s named time

    // COmpile a list of iterations for each core (list of lists)
    std::vector<std::vector<int>>iterations(p); // this creates a vector of size p with empty vectors inside named iterations 

    // Now that we have out data structures we can start assigning iterations to cores

    for(int i = n; i>=0; i--){
        // find core with minimum time
        int min_core = std::min_element(time.begin(), time.end()) - time.begin();

        // assign iteration i to min_core
        iterations[min_core].push_back(i);

        // update time for min_core
        time[min_core] += i;


    }

    // Print out the assignments
    for (int core = 0; core<p; core++){ // loop starting at core =0 while core is less than p
        std::cout << "Core " << core << ": (time = " << time[core] << ") " ;
        for (int it : iterations[core]){ // range based for loop
            std::cout << it << " ";
        
        }
        std::cout << std::endl;
    }
    

}


