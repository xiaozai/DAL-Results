close all; clear all;

% cdtb_path='/home.guest/yanliqia/mydatagrid/yanliqia/RGBD_benchmarks/Princeton_RGBD/EvaluationSet';
% cdtb_path='/Users/yanlinqian/yanliqia_cmp_datagrid/RGBD_benchmarks/Princeton_RGBD/EvaluationSet';
ptb_path = '/home/yan/Desktop/RGBD_benchmarks/Princeton_RGBD/EvaluationSet/';

trackers={'DIMP_results','DIMP_rgbd_blend2', 'OTR'};
trackers_color={'y','r', 'b'};

list_txt='./evaluation_list.txt';
list_sequences=textscan(fopen(list_txt), '%s','delimiter', '\n');
list_sequences=list_sequences{1};

for seq_id=1:numel(list_sequences)
    sequence = list_sequences{seq_id};
    
     % read bounding boxes
    fprintf('Processing bboxes from tarckers\n');
    
    tracker_bbox={}
    for tracker_id=1:numel(trackers)
        tracker_name=trackers{tracker_id}
        bbox_path=fullfile(tracker_name, sprintf('%s.txt', sequence));
        bboxes = dlmread(bbox_path);
        tracker_bbox{tracker_id}=bboxes;
    end
    
    for frame_id=1:size(bboxes,1)
        if mod(frame_id,2)~=0
            continue;
        else
            fprintf('Processing sequence: %s, %d/%d, \n', sequence,frame_id,size(bboxes,1));
            sequencename=list_sequences{seq_id};
            imgname=sprintf('rgb/*-%d.png',frame_id);
            img_fullpath=fullfile(ptb_path,sequencename,imgname);
            dir_img=dir(img_fullpath);
            img_fullpath=fullfile(ptb_path,sequencename,'rgb',dir_img(1).name);
            img=imread(img_fullpath);
            h=figure('visible', 'off'); 
            imshow(img,'border','tight');
            for tracker_id=1:numel(trackers)
                bbox_frame=tracker_bbox{tracker_id}(frame_id,:);
                bbox_frame(3)=bbox_frame(3)-bbox_frame(1);
                bbox_frame(4)=bbox_frame(4)-bbox_frame(2);
                if ~any(isnan(bbox_frame(:))) | any(bbox_frame,'all')
                hold on; rectangle('Position',bbox_frame,'Edgecolor',trackers_color{tracker_id},'LineWidth',4);
                end
            end
            img_savepath=strrep(img_fullpath,'rgb','visualcompare');
            img_savepath=strrep(img_savepath,'.png','.jpg');
            [folder_savepath,~,~] = fileparts( img_savepath);
            if ~exist(folder_savepath,'dir')
                mkdir(folder_savepath);
            end
            saveas(h,img_savepath);
            close(h);
        end
    end
    
    
end