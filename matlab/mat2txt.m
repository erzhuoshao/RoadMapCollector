function mat2txt(data, fid)
fid = fopen(fid, 'w');
for n=1:size(data, 2)
    for each = 1:size(data{n}, 1)
        fprintf(fid, '%d', data{n}(each, 1));
        fprintf(fid, ' ');
        fprintf(fid, '%d', data{n}(each, 2));
        if(each ~= length(data{n}))
            fprintf(fid, ' ');
        end
    end
    fprintf(fid, '\n');
end
fclose(fid);