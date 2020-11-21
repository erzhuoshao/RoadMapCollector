function pic = addframe(road_gray_high)
se3= strel('square',30);
road_gray_high_expand = imdilate(~road_gray_high,se3);
pic = ~ ((~road_gray_high_expand) | (~road_gray_high));