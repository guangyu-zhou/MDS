load('./dblp_4area_title')
[p_size, a_size] = size(Mda);

for i = 1:a_size
    k = strfind(name.author_name(i), 'Han')
    if  k > 0
        i
        break
    end
end