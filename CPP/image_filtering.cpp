
#include <opencv2/imgproc.hpp>
#include <opencv2/imgcodecs.hpp>
#include <iostream>
#include <vector>
#include <map>
#include <dirent.h>
#include <cstring>

// -o testoutput -std=c++11 `pkg-config --cflags --libs opencv`

using namespace std;
using namespace cv;


class Filtering {
    private:
        Mat filter;
        vector<Mat> data_array;
        vector<string> names;
        string low_or_high;
        string fname;
        map<int, int> center;
        bool dir;

    public:
        Filtering(string filename, Mat fltr, string low_high, bool directory)
        {
            // Assert file exists
            if (directory) {
                // Traverse through directory 
                dp = opendir(directory);
                if (dp != nullptr) {
                    while( ( entry = readdir(dp))) {
                        string name = entry->d_name;
                    }            
                }
            }
            else {
                Mat src = imread(filename);
                if (src.empty()){
                    printf("No such file!\n");
                    exit(0);
                }
                data_array.push_back(src);
                names.push_back(filename);
            }

            filter = fltr;
            fname = filename;
            low_or_high = low_high;
            dir = directory;

            //Create ranges

        }

        vector<Mat> filter(){
            
        }
};


int main( int argc, char ** argv){

    const char* filename = argv[1];

    Mat src = imread(filename);
    if (src.empty()){
        printf("Error opening image \n");
        return 0;
    }
    std::cout<<src;

    return 0;
}