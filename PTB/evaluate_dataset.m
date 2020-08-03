clear all;
dir_PTBgt    ='./ValidationSet';
dir_PTBresult='./ATOM_results';
seq_name='zcup_move_1';
thresh=0.5;%[0:0.01:1];

[succRate,TypeI,TypeII]=singleTestcaseEvaluation (dir_PTBresult,dir_PTBgt,seq_name,thresh);