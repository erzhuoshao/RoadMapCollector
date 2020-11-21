function road_gray = IPNV_read(inputpwd)
road_gray = imread(inputpwd);
if ~islogical(road_gray)
    level = graythresh(road_gray);
    road_gray = im2bw(road_gray);
end
road_gray = ~road_gray;
