load('./dblp_4area_title')
[p_size, a_size] = size(Mda);
% 
% % for paper = 5:10
% %     x= Mda(paper,:)
% % end
% x = Mda(10,:);
% authors = find(x(1,:));
% 

%  a = [1,0,0,0;0,1,0,1;1,1,1,0; 0,0,1,1; 0,0,1,1];
%  x = a'*a;

ata =  Mda'*Mda ;
ata = ata - diag(diag(ata));
[x,y,val] = find(ata);
authorCorrNew = ata;

%%% function for gen edge file %%%
% p = 0.2;
% 
% for i = 1:nnz(ata)
% %     if mod(i,10000) == 0
% %         i
% %     end
%     u = x(i);
%     v = y(i);
% %     au = nonzeros(sum(Mda(:,u)));
% %     av = nonzeros(sum(Mda(:,v)));
% %     authorCorr(u, v) = (p_size*val(i) - au*av)/(sqrt((p_size - au)*au)*sqrt((p_size- av)*av));
%     authorCorrNew(u, v) = 1 - (1-p).^val(i);
% %     break;
% end
% 
% [au,av,corr] = find(authorCorrNew);
% dlmwrite('authorCorr0.2.txt',[au,av, corr],'delimiter','\t');

%%% function for gen grapg file %%%
author_pair = sparse(a_size, a_size);
cur_author = 19495;
coauthorCovered = [cur_author];
Q = [cur_author];
clc;
while size(Q, 2) > 0
    size(Q,2)
    cur_author = Q(1);
    Q(1) = [];
    
    [x1,y1,val1] = find(ata(cur_author,:));
    coauthor = [];
    % coauthor_val = [];
    for i = 1:size(y1, 2)
        if val1(i) > 1
            coauthor(end+1) = y1(i);
    %         coauthor_val(end+1) = val1(i);
            author_pair(cur_author, y1(i)) = val1(i); 
            if ~ismember(y1(i), coauthorCovered)
                coauthorCovered(end+1) = y1(i);
                if val1(i) > 10
                    Q(end+1) = y1(i);
                end
            end
        end
    end
end
% author_pair
[a1,a2,commonPaper] = find(author_pair);
dlmwrite('aaNew10.txt',[a1,a2,commonPaper],'delimiter','\t');


