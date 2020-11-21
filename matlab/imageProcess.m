%% 图像处理大尺度简易版本V0
%% 参数设置
cityname = 'beijing';
maplevel = '12';
region_min_pixels = 50;

input_picture_path = ['../picture/', cityname, '-', maplevel, '.png'];
output_picture_path = ['../picture/', cityname, '-', maplevel, '-bone.png'];
output_pixel_path = ['../pixel/', cityname, '-', maplevel, '.txt'];
%% 1.0 读入数据，转换成灰度图片，提取测试单元
fprintf('1.0->读入数据，确定测试单元\n');
road_gray = addframe(IPNV_read(input_picture_path));
%% 2.0 膨胀腐蚀图像处理
fprintf('2.0->膨胀腐蚀图像处理\n');
if(~exist(output_picture_path, 'file'))
    road_imdilate = imdilate(road_gray, strel('square',5));
    road_skel = bwmorph(road_imdilate,'skel',Inf);
    road_spur = bwmorph(road_skel ,'spur',Inf);
    
    road_bone = bwareaopen(road_spur, 50);
    road_bone(:, 1) = 1;
    road_bone(1, :) = 1;
    road_bone(:, size(road_bone, 2)) = 1;
    road_bone(size(road_bone, 1), :) = 1;
    
    imwrite(road_bone, output_picture_path);
else
    road_bone = IPNV_read(output_picture_path);
end
%% 3.0 提取区域边界
fprintf('3.0->提取区域边界\n');
B_ch_o = bwboundaries(bwlabel(~road_bone));
B_ch = cell(1);
count = 0;
for n=1:length(B_ch_o)
    if(length(B_ch_o{n}) > region_min_pixels)
        count = count + 1;
        B_ch{count} = B_ch_o{n};
    end
end
mat2txt(B_ch, output_pixel_path);
