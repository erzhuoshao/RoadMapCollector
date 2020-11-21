inputpwd = '../picture/beijing/beijing0tmp.png';
grey = imread(inputpwd);
if ~islogical(grey)
    level = graythresh(grey);
    grey = im2bw(grey);
end
smaller = zeros(size(grey) / 10, 'logical');
for i = 1:size(smaller, 1)
    for j = 1:size(smaller, 2)
        if(min(grey((i - 1) * 10 + 1:i * 10, (j - 1) * 10 + 1:j * 10)))
            smaller(i, j) = 1;
        end
    end
end
imsave('../picture/beijing/smaller_beijing0tmp.png');