import sys
import cv2
import os
import numpy as np
import sys
import matplotlib


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
args = parser.parse_args()

if __name__ == '__main__':

    # 1) Loading Trackers and Sequences
    if args.tracker:
        trackers = args.tracker
    else:
        trackers = load_trackers_from_list(os.path.join(args.raw_results_path, 'trackers.txt'))
    print(trackers)

    if len(trackers):
        # create random colors for all trackers
        tracker_colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                            for i in range(len(trackers))]
        # color_names = [hex_to_name(t_color) for t_color in tracker_colors]

        # loading sequences
        if os.path.isdir(args.sequences_path):
            if args.sequence:
                vids = args.sequence
            else:
                vids = os.listdir(args.sequences_path)
                vids.remove('list.txt')
                vids.sort()
            num_vids = len(vids) # 80 Sequences

            # 2) Visualize the raw results for each tracker
            for vid, title in enumerate(vids[0:num_vids]):
                path = args.sequences_path + '{}'.format(title)
                # get the groundtruth
                gt_bbox = np.loadtxt(os.path.join(path, 'groundtruth.txt'), delimiter=',')
                # get the predicted bbox from trackers
                trackers_bbox = []
                for tracker in trackers:
                    prediction_bbox = np.loadtxt(os.path.join(args.raw_results_path, tracker, title, '{}_001.txt'.format(title)), delimiter=',')
                    trackers_bbox.append(prediction_bbox)
                # visualzie
                num = len(os.listdir(os.path.join(path, 'color')))

                plt.close()
                fig, ax = plt.subplots(1)
                fig.canvas.manager.window.wm_geometry("+%d+%d" % (200, 100))
                plt.tight_layout()
                # plt.title(title)

                for frame_i in range(num):
                    im = cv2.cvtColor(cv.imread(os.path.join(path, 'color/{:0>8d}.jpg'.format(frame_i + 1))), cv.COLOR_BGR2RGB)

                    ax.cla()
                    ax.imshow(im)

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
                            vis_bbox = patches.Rectangle((trackers_bbox[tracker_i][frame_i][0], trackers_bbox[tracker_i][frame_i][1]),
                                                          trackers_bbox[tracker_i][frame_i][2], trackers_bbox[tracker_i][frame_i][3],
                                                          linewidth=2, edgecolor=tracker_colors[tracker_i], facecolor='none')
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
