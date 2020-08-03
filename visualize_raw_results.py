import sys
import cv2
import os
import numpy as np
import sys
import matplotlib
import json


matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cv2 as cv
import random
import argparse
from webcolors import hex_to_name

def load_trackers_from_list(tracker_list):
    trackers = []

    if os.path.isfile(tracker_list):
        with open(tracker_list) as f:
            trackers = f.readlines()
        trackers = [x.strip() for x in trackers]
    elif os.path.isdir(tracker_list):
        trackers = os.listdir(tracker_list)

    return trackers

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--raw_results_path', default='/home/yan/Desktop/DAL-Results/CDTB/raw_results/',
                    help='the folder where saves the raw results from trackers')
parser.add_argument('--sequences_path', default='/home/yan/Projects/VOT-RGBD2020/vot-workspace/sequences/',
                    help='the path to sequences')
parser.add_argument('--tracker', default='', type=str, nargs='+',
                    help='for one specific tracker')
parser.add_argument('--sequence', default='', type=str, nargs='+',
                    help='for one specific sequence')
parser.add_argument('--savefig', default=False, type=bool,
                    help='save the visualized image with predicted bboxes')
parser.add_argument('--dataset', default='PTB', type=str,
                    help=' [PTB, CDTB, STC]')
args = parser.parse_args()

if __name__ == '__main__':

    # 1) Loading Trackers and Sequences
    if args.tracker:
        trackers = args.tracker
    else:
        try:
            trackers = load_trackers_from_list(os.path.join(args.raw_results_path, 'trackers.txt'))
        except:
            trackers = []
            print('no trackers')
    print(trackers)

    if len(trackers):
        # create random colors for all trackers
        tracker_colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                            for i in range(len(trackers))]
        # loading sequences
        if os.path.isdir(args.sequences_path):
            if args.sequence:
                vids = args.sequence
            else:
                vids = os.listdir(args.sequences_path)
                if args.dataset == 'CDTB':
                    vids.remove('list.txt')
                elif args.dataset == 'STC':
                    vids.remove('benchmark_name.txt')
                    vids.remove('.directory')
                vids.sort()
            num_vids = len(vids) # 80 Sequences for CDTB, 95 seqs for PTB , 36 for STC
            
            # 2) Visualize the raw results for each tracker
            for vid, title in enumerate(vids[0:num_vids]):
                seq_path = args.sequences_path + '{}'.format(title)
                # get the groundtruth
                gt_exists = False
                if os.path.isfile(os.path.join(seq_path, 'groundtruth.txt')):
                    gt_exists = True
                    gt_bbox = np.loadtxt(os.path.join(seq_path, 'groundtruth.txt'), delimiter=',')
                # get the predicted bbox from trackers
                trackers_bbox = []
                for tracker in trackers:
                    # in CDTB (VOT), output files are seqName_001.txt, seqName_001_confidence.txt , seqName_001_time.txt
                    if args.dataset == 'CDTB':
                        if os.path.isfile(os.path.join(args.raw_results_path, tracker, title, '{}_001.txt'.format(title))):
                            prediction_txt = os.path.join(args.raw_results_path, tracker, title, '{}_001.txt'.format(title))
                    # in PTB results, these files are all in one folder, and namely seqName.txt
                    elif args.dataset == 'PTB' or args.dataset == 'STC':
                        if os.path.isfile(os.path.join(args.raw_results_path, tracker, '{}.txt'.format(title))):
                            prediction_txt = os.path.join(args.raw_results_path, tracker, '{}.txt'.format(title))
                        elif os.path.isfile(os.path.join(args.raw_results_path, tracker, '{}_{}.txt'.format(tracker, title))):
                            prediction_txt = os.path.join(args.raw_results_path, tracker, '{}_{}.txt'.format(tracker, title))
                    else:
                        prediction_txt = ''
                        print(' Tracker : {}, Seq : {}, Prediction not exists'.format(tracker, title))

                    if prediction_txt:
                        try:
                            prediction_bbox = np.loadtxt(prediction_txt, delimiter=',')
                        except:
                            prediction_bbox = np.loadtxt(prediction_txt, delimiter='\t')
                        trackers_bbox.append(prediction_bbox)
                # visualzie
                if args.dataset == 'CDTB':
                    im_path = os.path.join(seq_path, 'color')
                elif args.dataset == 'PTB':
                    im_path = os.path.join(seq_path, 'rgb')
                elif args.dataset == 'STC':
                    im_path = os.path.join(seq_path, 'RGB')
                else:
                    im_path = seq_path

                # For PTB , image name is r-timesstamp-frameID , e.g. r-0-1
                # For CDTB and STC, image name is 0>8d.jpg or png
                frames = []
                if args.dataset == 'PTB':
                    json_file = os.path.join(seq_path, 'frames.json')
                    if os.path.isfile(json_file):
                        with open(json_file) as f:
                            json_data = json.load(f)
                        imageTimestamp = json_data['imageTimestamp']
                        imageFrameID = json_data['imageFrameID']
                        for ii in range(0, len(imageFrameID)):
                            im_name = 'r-{}-{}.png'.format(imageTimestamp[ii], imageFrameID[ii])
                            frames.append(im_name)
                elif args.dataset == 'CDTB':
                    for ii in range(0, len(os.listdir(im_path))):
                        im_name = '{:0>8d}.jpg'.format(ii + 1)
                        frames.append(im_name)
                elif args.dataset == 'STC':
                    for ii in range(0, len(os.listdir(im_path))):
                        im_name = '{:0>8d}.png'.format(ii + 1)
                        frames.append(im_name)

                plt.close()
                fig, ax = plt.subplots(1)
                fig.canvas.manager.window.wm_geometry("+%d+%d" % (200, 100))
                plt.tight_layout()

                for frame_i, frame_name in enumerate(frames[0:len(frames)]):
                    im = cv2.cvtColor(cv.imread(os.path.join(im_path, frames[frame_i])), cv.COLOR_BGR2RGB)

                    ax.cla()
                    ax.imshow(im)

                    if gt_exists:
                        if len(gt_bbox[frame_i])==4:
                            vis_gt_bbox = patches.Rectangle((gt_bbox[frame_i][0], gt_bbox[frame_i][1]),
                                                            gt_bbox[frame_i][2], gt_bbox[frame_i][3],
                                                            linewidth=2, edgecolor='r', facecolor='none')
                            ax.add_patch(vis_gt_bbox)
                        elif len(gt_bbox[frame_i])==8:
                            print('GT is polygon')

                        # add GT labels
                        plt.text(gt_bbox[frame_i][0], gt_bbox[frame_i][1], '0', fontsize=8, color='r')
                        plt.text(40, 10, ' 0 - GT', fontsize=6, color='k')
                        gt_rect = patches.Rectangle((10, 5), 25, 5, facecolor='r')
                        ax.add_patch(gt_rect)

                    for tracker_i in range(len(trackers)):
                        if len(trackers_bbox[tracker_i][frame_i])==4:
                            # # For PTB , (target_top_left_x,target_top_left_y,target_down_right_x,target_down_right_y)
                            if args.dataset == 'PTB':
                                x = trackers_bbox[tracker_i][frame_i][0]
                                y = trackers_bbox[tracker_i][frame_i][1]
                                w = trackers_bbox[tracker_i][frame_i][2] - trackers_bbox[tracker_i][frame_i][0]
                                h = trackers_bbox[tracker_i][frame_i][3] - trackers_bbox[tracker_i][frame_i][1]
                            # # For CDTB and also STC , (x, y, w, h)
                            elif args.dataset == 'CDTB' or args.dataset == 'STC':
                                x = trackers_bbox[tracker_i][frame_i][0]
                                y = trackers_bbox[tracker_i][frame_i][1]
                                w = trackers_bbox[tracker_i][frame_i][2]
                                h = trackers_bbox[tracker_i][frame_i][3]
                            else:
                                x, y, w, h = 0, 0, 0, 0

                            vis_bbox = patches.Rectangle((x, y), w, h, linewidth=2, edgecolor=tracker_colors[tracker_i], facecolor='none')
                            ax.add_patch(vis_bbox)
                            plt.text(trackers_bbox[tracker_i][frame_i][0], trackers_bbox[tracker_i][frame_i][1], ' %d'%(tracker_i+1), fontsize=6, color=tracker_colors[tracker_i])
                        elif len(trackers_bbox[tracker_i][frame_i])==8:
                            print('Prediction is Polygon')

                        # add tracker labels
                        plt.text(40, (tracker_i+1)*20+10, ' %d - %s'%(tracker_i+1, trackers[tracker_i]), fontsize=8, color='k')
                        tracker_rect = patches.Rectangle((10, tracker_i*20+26), 25, 5, facecolor=tracker_colors[tracker_i])
                        ax.add_patch(tracker_rect)

                    ax.set_axis_off()
                    ax.axis('equal')
                    plt.draw()
                    plt.pause(0.001)
