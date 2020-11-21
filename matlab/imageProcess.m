%% ͼ�����߶ȼ��װ汾V0
%% ��������
cityname = 'beijing';
maplevel = '12';
region_min_pixels = 50;

input_picture_path = ['../picture/', cityname, '-', maplevel, '.png'];
output_picture_path = ['../picture/', cityname, '-', maplevel, '-bone.png'];
output_pixel_path = ['../pixel/', cityname, '-', maplevel, '.txt'];
%% 1.0 �������ݣ�ת���ɻҶ�ͼƬ����ȡ���Ե�Ԫ
fprintf('1.0->�������ݣ�ȷ�����Ե�Ԫ\n');
road_gray = addframe(IPNV_read(input_picture_path));
%% 2.0 ���͸�ʴͼ����
fprintf('2.0->���͸�ʴͼ����\n');
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
%% 3.0 ��ȡ����߽�
fprintf('3.0->��ȡ����߽�\n');
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
