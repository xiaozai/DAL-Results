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

def load_trackers_and_colors(params):
    ''' Load the list of the specific trackers from the txt or all trackers in the folder'''
    trackers = []

    if params.tracker:
        # if there are specific tracekrs
        trackers = params.tracker
    else:
        tracker_list = os.path.join(params.raw_results_path, 'trackers.txt')
        if os.path.isfile(tracker_list):
            with open(tracker_list) as f:
                trackers = f.readlines()
            trackers = [x.strip() for x in trackers]
        elif os.path.isdir(params.raw_results_path):
            # if no list, get all sub-directories in the raw results folder
            trackers = [f for f in os.listdir(params.raw_results_path) if os.path.isdir(os.path.join(params.raw_results_path, f))]
        else:
            trackers = []
            print('no trackers')
    # create random colors for all trackers
    tracker_colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(trackers))] if len(trackers) else []
    print(trackers)
    return trackers, tracker_colors, len(trackers)

def load_sequences_names(params):
    ''' Load the names of sequences from the folder or the input list '''
    vids = []
    if os.path.isdir(params.sequences_path):
        if params.sequence:
            vids = params.sequence
        else:
            vids = os.listdir(params.sequences_path)
            if params.dataset == 'CDTB':
                vids.remove('list.txt')
            elif params.dataset == 'STC':
                vids.remove('benchmark_name.txt') # Or can load the seq list from benchmark_name.txt
                vids.remove('.directory')         # no idea why it is here
            vids.sort()
    print('Totally %d sequences '%len(vids))
    return vids, len(vids) # Totally 80 Sequences for CDTB, 95 seqs for PTB , 36 for STC

parser = argparse.ArgumentParser(description='Please specify the raw results path and the sequences path')
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
parser.add_argument('--save_path', default='', type=str,
                    help='save the visualized images with predicted bboxes')
parser.add_argument('--dataset', default='PTB', type=str,
                    help='[PTB, CDTB, STC]')
args = parser.parse_args()

if __name__ == '__main__':

    # 1) Loading Trackers and Sequences
    trackers, tracker_colors, num_trackers = load_trackers_and_colors(args)

    if num_trackers:
        # loading sequences
        vids, num_vids = load_sequences_names(args)
        if num_vids:
            # 2) Visualize the raw results for each tracker
            for vid, title in enumerate(vids[0:num_vids]):

                if args.savefig and args.save_path:
                    if not os.path.isdir(os.path.join(args.save_path, title)):
                        os.mkdir(os.path.join(args.save_path, title))

                seq_path = os.path.join(args.sequences_path, title)

                # get the groundtruth , it is for CDTB dataset, no GT for PTB, and STC has the GT folder for all seqs
                gt_exists = False
                if os.path.isfile(os.path.join(seq_path, 'groundtruth.txt')):
                    gt_exists = True
                    gt_bbox = np.loadtxt(os.path.join(seq_path, 'groundtruth.txt'), delimiter=',')
                # get the predicted bbox from trackers
                trackers_bbox = []
                for tracker in trackers:
                    # in CDTB (VOT challenge), output files are seqName_001.txt, seqName_001_confidence.txt , seqName_001_time.txt
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
                            # Some trackers output predicted bbox like (x    y     w    h), e.g. DiMP and DAL in STC
                            prediction_bbox = np.loadtxt(prediction_txt, delimiter='\t')
                        trackers_bbox.append(prediction_bbox)

                # difference folders for rgb images in each dataset
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

                    # Add GT bbox if exists
                    if gt_exists:
                        if len(gt_bbox[frame_i])==4:
                            if args.dataset == 'CDTB' or args.dataset == 'STC':
                                gt_x, gt_y, gt_w, gt_h = gt_bbox[frame_i]
                            elif args.dataset == 'PTB':
                                gt_x, gt_y, gt_xr, gt_yr = gt_bbox[frame_i]
                                gt_w = gt_xr - gt_x
                                gt_h = gt_yr - gt_y
                            else:
                                gt_x, gt_y, gt_w, gt_h = 0, 0, 0, 0
                                print('gt dataset not exists..')
                            vis_gt_bbox = patches.Rectangle((gt_x, gt_y), gt_w, gt_h, linewidth=2, edgecolor='r', facecolor='none')
                            ax.add_patch(vis_gt_bbox)
                        elif len(gt_bbox[frame_i])==8:
                            print('GT is polygon, not implemented yet ...')

                        # add GT labels
                        plt.text(gt_bbox[frame_i][0], gt_bbox[frame_i][1], '0', fontsize=8, color='r')
                        plt.text(40, 10, ' 0 - GT', fontsize=6, color='k')
                        gt_rect = patches.Rectangle((10, 5), 25, 5, facecolor='r')
                        ax.add_patch(gt_rect)

                    for tracker_i in range(len(trackers)):
                        if len(trackers_bbox[tracker_i][frame_i])==4:
                            if args.dataset == 'PTB':
                                # For PTB , (target_top_left_x,target_top_left_y,target_down_right_x,target_down_right_y)
                                x, y, xr, yr = trackers_bbox[tracker_i][frame_i]
                                w = xr - x
                                h = yr - y
                            elif args.dataset == 'CDTB' or args.dataset == 'STC':
                                # For CDTB and also STC , (x, y, w, h)
                                x, y, w, h = trackers_bbox[tracker_i][frame_i]
                            else:
                                x, y, w, h = 0, 0, 0, 0
                                print('prediction dataset not exists..')

                            vis_bbox = patches.Rectangle((x, y), w, h, linewidth=2, edgecolor=tracker_colors[tracker_i], facecolor='none')
                            ax.add_patch(vis_bbox)
                            plt.text(trackers_bbox[tracker_i][frame_i][0], trackers_bbox[tracker_i][frame_i][1], ' %d'%(tracker_i+1), fontsize=6, color=tracker_colors[tracker_i])
                        elif len(trackers_bbox[tracker_i][frame_i])==8:
                            print('Prediction is Polygon, not implemented yet ...')

                        # add tracker labels
                        plt.text(40, (tracker_i+1)*20+10, ' %d - %s'%(tracker_i+1, trackers[tracker_i]), fontsize=8, color='k')
                        tracker_rect = patches.Rectangle((10, tracker_i*20+26), 25, 5, facecolor=tracker_colors[tracker_i])
                        ax.add_patch(tracker_rect)

                    ax.set_axis_off()
                    ax.axis('equal')
                    plt.draw()
                    plt.pause(0.001)

                    # save current fig
                    if args.savefig and args.save_path:
                        plt.savefig(os.path.join(args.save_path, title, frames[frame_i]))
