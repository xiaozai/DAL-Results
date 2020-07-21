# formulate the raw results into
#  seq/seq_001.txt
#  seq/seq_001_confidence.txt
#  seq/seq_001_time.txt
#
#  x,y,w,h ..... instead of x y w h
import os
import numpy as np
from io import StringIO

def load_trackers_from_list(tracker_list):
    trackers = []

    if os.path.isfile(tracker_list):
        with open(tracker_list) as f:
            trackers = f.readlines()
        trackers = [x.strip() for x in trackers]
    elif os.path.isdir(tracker_list):
        trackers = os.listdir(tracker_list)

    return trackers


if __name__ == '__main__':

    raw_results_path = '/home/yan/Desktop/DAL-Results/CDTB/raw_results/'
    tracker_list = raw_results_path + 'trackers.txt'
    trackers = load_trackers_from_list(tracker_list)
    print('totally %d trackers '%len(trackers))

    sequences_path = '/home/yan/Projects/VOT-RGBD2020/vot-workspace/sequences/'
    vids = os.listdir(sequences_path)
    vids.remove('list.txt')
    vids.sort()
    print('totally %d sequences '%len(vids))

    for tracker in trackers:
        print('Tracker : %s'%tracker)

        tracker_result_path = os.path.join(raw_results_path, tracker)

        for seq in vids:
            seq_path = os.path.join(tracker_result_path, seq)

            # move files into sub-folders
            if not os.path.isdir(seq_path):
                os.mkdir(seq_path)

            if not len(os.listdir(seq_path)):
                try:
                    os.popen('mv %s.txt %s'%(tracker_result_path+'/'+seq, seq_path))
                except:
                    # print('mv %s_bboxes.txt %s'%(tracker_result_path+'/'+seq, seq_path))
                    os.popen('mv %s_bboxes.txt %s'%(tracker_result_path+'/'+seq, seq_path))
                finally:
                    print('Error mv %s*.txt %s is already in'%(tracker_result_path+'/'+seq, seq_path))

                try:
                    os.popen('mv %s_scores.txt %s'%(tracker_result_path+'/'+seq, seq_path))
                except:
                    print('Error : mv scores files : %s'%seq_path)

                try:
                    os.popen('mv %s_time.txt %s'%(tracker_result_path+'/'+seq, seq_path))
                except:
                    print('Error : mv time files : %s'%seq_path)

            # Re-write the predicted bbox file
            if os.path.isfile(os.path.join(seq_path, '%s_bboxes.txt'%seq)):
                result_bbox_file = os.path.join(seq_path, '%s_bboxes.txt'%seq)
            elif os.path.isfile(os.path.join(seq_path, '%s.txt'%seq)):
                result_bbox_file = os.path.join(seq_path, '%s.txt'%seq)
            else:
                print('can not find file:  %s or _bboxes.txt'%os.path.join(seq_path, seq+'.txt'))

            s = open(result_bbox_file).read().replace('\t',',')

            try:
                predicted_bbox = np.loadtxt(StringIO(s), delimiter=' ')
            except:
                predicted_bbox = np.loadtxt(StringIO(s), delimiter=',')

            with open(os.path.join(seq_path, '%s_001.txt'%seq), 'w') as f:
                for bbox in predicted_bbox:
                    f.write('%f,%f,%f,%f\n'%(bbox[0], bbox[1], bbox[2], bbox[3]))

            # Rename the confidence and time files
            try:
                os.rename(r'%s'%os.path.join(seq_path, seq+'_score.txt'), r'%s'%os.path.join(seq_path, seq+'_001_confidence.txt'))
            except:
                print('rename error : %s'%os.path.join(seq_path, seq+'_scores.txt'))

            try:
                os.rename(r'%s'%os.path.join(seq_path, seq+'_time.txt'), r'%s'%os.path.join(seq_path, seq+'_001_time.txt'))
            except:
                print('rename error, may no file exits : %s '%os.path.join(seq_path, seq+'_time.txt'))
