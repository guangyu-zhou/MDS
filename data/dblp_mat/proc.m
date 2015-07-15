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

ata0 =  Mda'*Mda ;
ata = ata - diag(diag(ata));
[x,y,val] = find(ata);
authorCorrNew = ata;

% aSum = zeros(a_size);
% for i = 1:a_size
%      = nonzeros(sum(Mda(:,10)))
% end

for i = 1:nnz(ata)
%     if mod(i,10000) == 0
%         i
%     end
    u = x(i);
    v = y(i);
%     au = nonzeros(sum(Mda(:,u)));
%     av = nonzeros(sum(Mda(:,v)));
%     authorCorr(u, v) = (p_size*val(i) - au*av)/(sqrt((p_size - au)*au)*sqrt((p_size- av)*av));
    authorCorrNew(u, v) = 1 - (1-0.1).^val(i);
%     break;
end
% save('authorCorr.mat', 'authorCorr');

[au,av,corr] = find(authorCorrNew);
dlmwrite('authorCorrNew.1.txt',[au,av,corr],'delimiter','\t');




