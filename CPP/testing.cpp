#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgcodecs.hpp>
#include <iostream>
#include <vector>
#include <map>
#include <dirent.h>
#include <cstring>
#include <opencv2/core/hal/interface.h>


using namespace std;
using namespace cv;

int main(){
    Mat img = imread("../IMAGES/brainMRI_1.jpg",cv::IMREAD_COLOR);
    waitKey(0);
    uint8_t *myData = img.data;

    //Process
    // Define filter 
    Mat1d filter = Mat1d::zeros(3, 3);
    filter << 3,3,3,3,3,3,3,3,3;
    cout<<filter;
    int sumatoria, row, col = 0;

    int lim_row = 3;
    int lim_col = 3;
    map<int, int, int> averages;

    while(true){
        int k, m = 0;
        for(int i = row; i < lim_row; i++){
            for(int j = col; j< lim_col; j++){
                sumatoria += filter(k, m)*myData[i, j];
                m += 1;
            }
            k += 1;
        }
        cout<<sumatoria;
        // averages[(lim_row - 1), (lim_col - 1)] = sumatoria;
        col += 1;
        lim_col += 1;

        if (lim_col > img.size[1]){
            row += 1;
            lim_row += 1;
            col = 0;
            lim_col = 3;
        }

        if (lim_row > img.size[0]){
            break;
        }
        cout<<sumatoria;
        sumatoria = 0;
    }

}