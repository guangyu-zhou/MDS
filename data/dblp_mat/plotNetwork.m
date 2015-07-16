% cm = ata;
% ids = name.author_name;
% bg = biograph(cm, ids);
% get(bg.nodes,'ID')

cm = author_pair;
% ids = {'M30931','L07625','K03454','M27323','M15390'};
bg2 = biograph(cm);
% get(bg2.nodes,'ID')
size(author_pair)
view(bg2)