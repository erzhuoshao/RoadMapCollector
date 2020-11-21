# RoadMapCollector

## Environment:
* Windows 10
* Python==3.7.0
* Pillow==8.0.1
* selenium==3.141.0
* Google Chrome 87.0.4280.66
* MATLAB R2019b

## Pipeline:
0. Select target city and maplevel
   1. cityname = 'beijing'
   2. maplevel = 12 # not greater than 19, the higher, the finer(Please refer to [BaiduMapAPI](http://api.map.baidu.com/lbsapi/getpoint/index.html)).
1. python main.py cityname maplevel
   1. Obtain boundary position of cityname
   1. Obtain patches in ./patch/cityname-maplevel.
   2. Obtain pasted road network picture/cityname-maplevel.png.
2. run imageProcess.m
   1. processing road network picture. Obtain pixel position of road network pixel/beijing-12.txt
3. (Optional) python corner.py cityname maplevel
   1. Simplified the pixel-level edge by corner detection. Obtain pixel/beijing-12-simplified.txt
4. python pixel2coor.py cityname maplevel
   1. Utilizing baiduAPI to transform pixel-level position to longitude and latitude. Obtain coor/beijing-12-simplified.txt
5. (Optional) python coorTransform.py cityname maplevel
   1. Transform coordinates from bd09 to gcj02. -> coor/beijing-12-simplified-gcj.txt
   
## Examples:
<img src="https://github.com/shaoerzhuo/RoadMapCollector/blob/main/patch/beijing-12/2-3.png" width="50%" height="50%">
<img src="https://github.com/shaoerzhuo/RoadMapCollector/blob/main/picture/beijing-12-simplified.png" width="50%" height="50%">

## Author:
* Erzhuo Shao and Jie Feng
* Erzhuo Shao: Wechat : shaoerzhuo, E-mail : sez20@mails.tsinghua.edu.cn
* Jie Feng : E-mail : fengj12ee@hotmail.com
