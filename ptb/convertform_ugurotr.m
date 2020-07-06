clear all;close all;
txt_seqlist='./validation_list.txt';


%% loop over seq list to generate PTB results.
seqlist=textread(txt_seqlist,'%s');
for seqind=1:length(seqlist)
    seqname=seqlist{seqind};
    seq_fullname=fullfile('./ValidationSet',[seqname])
    
    old_rgb_folder=fullfile(seq_fullname,'rgb/');
    old_depth_folder=fullfile(seq_fullname,'depth/');
    new_rgb_folder=fullfile(seq_fullname,'color/');
    new_depth_folder=fullfile(seq_fullname,'depth_new/');
    
    mkdir(new_rgb_folder);mkdir(new_depth_folder);
    
    old_rgb_files=dir([old_rgb_folder 'r-*-*.png']);
    old_rgb_files={old_rgb_files.name};
    old_rgb_files=natsortfiles(old_rgb_files);
    
    old_depth_files=dir([old_depth_folder 'd-*-*.png']);
    old_depth_files={old_depth_files.name};
    old_depth_files=natsortfiles(old_depth_files);
    
    for img_ind=1:length(old_rgb_files)
        img_ind
        old_rgb_file=old_rgb_files{img_ind};
        old_depth_file=old_depth_files{img_ind};
        new_rgb_file=sprintf('Color_%08d.png',img_ind-1);
        new_depth_file=strrep(new_rgb_file,'Color_','Depth_');
        
        copyfile([old_rgb_folder old_rgb_file], [new_rgb_folder new_rgb_file]);
        copyfile([old_depth_folder old_depth_file], [new_depth_folder new_depth_file]);
    end
end