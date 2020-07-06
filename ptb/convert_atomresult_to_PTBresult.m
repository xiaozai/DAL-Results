clear all;close all;
txt_seqlist='./evaluation_list.txt';
dir_atomresult='/Users/yanlinqian/yanliqia_cmp_datagrid/pytracking_dimp/pytracking/tracking_results/dimp_rgbd_blend2/dimp50_ptb/';
dir_savePTBresult='./DIMP_rgbd_blend2/';
mkdir(dir_savePTBresult);

%% loop over seq list to generate PTB results.
seqlist=textread(txt_seqlist,'%s');
for seqind=1:length(seqlist)
    seqname=seqlist{seqind};
    seq_fullname=fullfile(dir_atomresult,[seqname,'.txt'])
    [x1,y1,w,h]=textread(seq_fullname,'%d\t%d\t%d\t%d\t');
    
    x2=x1+w;
    y2=y1+h;
    
    ind_nan=w==0;
    x2(ind_nan)=nan;
    y2(ind_nan)=nan;
    x1(ind_nan)=nan;
    y1(ind_nan)=nan;
    
    ptbresult_fullname=fullfile(dir_savePTBresult, [seqname,'.txt']);
    csvwrite(ptbresult_fullname,[x1,y1,x2,y2]);
end