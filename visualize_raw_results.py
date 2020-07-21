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
parser.add_argument('raw_results_path', default='/home/yan/Desktop/DAL-Results/CDTB/raw_results/',
                    help='the folder where saves the raw results from trackers')
parser.add_argument('sequences_path', default='/home/yan/Projects/VOT-RGBD2020/vot-workspace/sequences/',
                    help='the path to sequences')
args = parser.parse_args()

if __name__ == '__main__':

    # 1) Loading Trackers and Sequences
    trackers = load_trackers_from_list(os.path.join(args.raw_results_path, 'trackers.txt'))

    if len(trackers):
        # create random colors for all trackers
        tracker_colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                            for i in range(len(trackers))]
        # loading sequences
        if os.path.isdir(args.sequences_path):
            vids = os.listdir(args.sequences_path)
            vids.remove('list.txt')
            vids.sort()
            num_vids = length(vids) # 80 Sequences

            # 2) Visualize the raw results for each tracker
            for vid, title in enumerate(vids[0:num_vids]):
                path = args.sequences_path + '{}'.format(title)
                # get the groundtruth
                gt_bbox = np.loadtxt(os.path.join(path, 'groundtruth.txt'), delimiter=',')
                # get the predicted bbox from trackers
                trackers_bbox = []
                for tracker in trackers:
                    prediction_bbox = np.loadtxt(os.path.join(args.raw_results_path, tracker, '{}.txt'.format(title)), delimiter=',')
                    trackers_bbox.append(prediction_bbox)
                # visualzie
                num = len(os.listdir(os.path.join(path, 'color')))

                plt.close()
                fig, ax = plt.subplots(1)
                fig.canvas.manager.window.wm_geometry("+%d+%d" % (100, 50))
                plt.tight_layout()

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

                    for tracker_i in range(len(trackers)):
                        if len(trackers_bbox[tracker_i][frame_i])==4:
                            vis_bbox = patches.Rectangle((trackers_bbox[tracker_i][frame_i][0], trackers_bbox[tracker_i][frame_i][1]),
                                                          trackers_bbox[tracker_i][frame_i][2], trackers_bbox[tracker_i][frame_i][3],
                                                          linewidth=2, edgecolor=tracker_colors[tracker_i], facecolor='none')
                            ax.add_patch(vis_bbox)
                        elif len(trackers_bbox[tracker_i][frame_i])==8:
                            print('Prediction is Polygon')

                    ax.set_axis_off()
                    ax.axis('equal')
                    plt.draw()
                    plt.pause(0.001)



# tracker_name = 'D3S'
# experiment_name = 'baseline'
# workspace_path = '/home/yan/Data2/VOT_RGB_2020/d3s/vot-workspace-vot2018'
# vids = os.listdir(workspace_path + '/' + 'sequences')
# vids.remove('list.txt')
# vids.sort()

# results_dir = workspace_path + '/' + 'results'
#
# params = vot_params.parameters()
# params.masks_save_path = ''
# params.save_mask = False
#
# tracker = Segm(params)
#
# for vid, title in enumerate(vids[0:80]):
#     path = workspace_path + '/sequences/{}'.format(title)
#     num = len(os.listdir(os.path.join(path, 'color')))
#
#     base_results_path = '{}/{}/{}/{}'.format(results_dir, tracker_name, experiment_name, title)
#     results_path = '{}/{}_001.txt'.format(base_results_path, title)
#     # Check if results exist, skip this seq
#     if os.path.isfile(results_path):
#         print('{:0>2d} Tracker: {} ,  Sequence: {}'.format(vid, tracker_name, title))
#         continue
#
#     gt_list = np.loadtxt(os.path.join(path, 'groundtruth.txt'), delimiter=',')
#
#     box_list, polygon_list, confidence_list, time_list = [], [], [], []
#
#     for frame_i in range(0, num):
#         im = cv2.cvtColor(cv.imread(os.path.join(path, 'color/{:0>8d}.jpg'.format(frame_i + 1))), cv.COLOR_BGR2RGB)
#         # im_d = cv.imread(os.path.join(path, 'depth/{:0>8d}.png'.format(frame_i + 1)), cv.IMREAD_GRAYSCALE)
#         tic = time.time()
#         if frame_i == 0:
#             # x, y, w, h = gt_list[frame_i]
#             # gt_rect = rect_to_poly([x,y,w,h])
#             # gt_rect = gt_list[frame_i]
#
#             if len(gt_list[frame_i]) == 8:
#                 gt_poly = gt_list[frame_i]
#             else:
#                 print('Gt is rect ...., convert into poly ..')
#                 gt_poly = rect_to_poly(gt_list[frame_i])
#
#             # # tell the sequence name to the tracker (to save segmentation masks to the disk)
#             tracker.sequence_name = title
#             tracker.frame_name = '{:0>8d}'.format(frame_i+1)
#             tracker.initialize(im, gt_poly)
#
#             # Save the first results
#             box_list.append('1\n')
#             polygon_list.append('1\n')
#             confidence_list.append('\n')
#             time_list.append('{:.6f}\n'.format(time.time() - tic))
#
#             if visualize_flag:
#                 plt.close()
#                 fig, ax = plt.subplots(1)
#                 fig.canvas.manager.window.wm_geometry("+%d+%d" % (100, 50))
#                 plt.tight_layout()
#
#                 ax.cla()
#                 ax.imshow(im)
#
#                 vis_gt_polygon = patches.Polygon([(gt_poly[0], gt_poly[1]),
#                                                   (gt_poly[2], gt_poly[3]),
#                                                   (gt_poly[4], gt_poly[5]),
#                                                   (gt_poly[6], gt_poly[7])],
#                                                   linewidth=2, edgecolor='b', facecolor='none')
#                 ax.add_patch(vis_gt_polygon)
#                 ax.set_axis_off()
#                 ax.axis('equal')
#                 plt.draw()
#                 plt.pause(0.001)
#         else:
#             # Perform tracking
#             prediction = tracker.track(im)   # polygon
#
#             if len(prediction) == 4:
#                 print('Output is bbox .......')
#                 prediction_rect = prediction
#                 prediction_poly = rect_to_poly(prediction)
#
#             elif len(prediction) == 8:
#                 # get axis-align bbox from polygon
#                 shapes = [Polygon([(prediction[0], prediction[1]),
#                                    (prediction[2], prediction[3]),
#                                    (prediction[4], prediction[5]),
#                                    (prediction[6], prediction[7])])]
#                 bbox = BoundingBox.from_shapes(shapes)
#                 center, w, h = bbox.center, bbox.width, bbox.height
#                 x = center[0] - w / 2.0
#                 y = center[1] - h / 2.0
#                 # for visualization
#                 prediction_rect = [x,y,w,h]
#                 prediction_poly = prediction
#
#             # save the prediction bbox and polygon
#             box_list.append('{:.4f},{:.4f},{:.4f},{:.4f}\n'.format(
#                 prediction_rect[0], prediction_rect[1], prediction_rect[2], prediction_rect[3]))
#             polygon_list.append('{:.4f},{:.4f},{:.4f},{:.4f}{:.4f},{:.4f},{:.4f},{:.4f}\n'.format(
#                 prediction_poly[0],prediction_poly[1],prediction_poly[2],prediction_poly[3],
#                 prediction_poly[4],prediction_poly[5],prediction_poly[6],prediction_poly[7]))
#
#             # visualize
#             if visualize_flag:
#                 ax.cla()
#                 ax.imshow(im)
#                 # Rectangle : x, y, width, height
#                 vis_bbox = patches.Rectangle((prediction_rect[0], prediction_rect[1]),
#                                               prediction_rect[2], prediction_rect[3],
#                                              linewidth=2, edgecolor='r', facecolor='none')
#                 ax.add_patch(vis_bbox)
#                 # Polygon : 4 points, (x, y)
#                 vis_poly = patches.Polygon([(prediction_poly[0], prediction_poly[1]),
#                                             (prediction_poly[2], prediction_poly[3]),
#                                             (prediction_poly[4], prediction_poly[5]),
#                                             (prediction_poly[6], prediction_poly[7])],
#                                             linewidth=2, edgecolor='b', facecolor='none')
#                 ax.add_patch(vis_poly)
#
#                 if len(gt_list[frame_i]) == 4:
#                     print('Gt is rect bbox .....')
#                     gt_x, gt_y, gt_w, gt_h = gt_list[frame_i]
#                     gt_bbox = patches.Rectangle((gt_x, gt_y), gt_w, gt_h, linewidth=2, edgecolor='g', facecolor='none')
#                     ax.add_patch(gt_bbox)
#                 else:
#                     gt_polygon = patches.Polygon([(gt_list[frame_i][0], gt_list[frame_i][1]),
#                                                   (gt_list[frame_i][2], gt_list[frame_i][3]),
#                                                   (gt_list[frame_i][4], gt_list[frame_i][5]),
#                                                   (gt_list[frame_i][6], gt_list[frame_i][7])],
#                                                   linewidth=2, edgecolor='g', facecolor='none')
#                     ax.add_patch(gt_polygon)
#                 ax.set_axis_off()
#                 ax.axis('equal')
#                 plt.draw()
#                 plt.pause(0.001)
#             else:
#                 print('unknow prediction ')
#                 continue
#
#             confidence_list.append('{:.2f}\n'.format(1))
#             time_list.append('{:.6f}\n'.format(time.time() - tic))
#
#     print('{:0>2d} Tracker: {} ,  Sequence: {}'.format(vid, tracker_name, title))
#
#     vid_path = os.path.join(results_dir, tracker_name, experiment_name, '{:s}'.format(title))
#     if not os.path.exists(vid_path):
#         os.makedirs(vid_path)
#
#     # save box
#     if len(box_list) > 0:
#         with open(os.path.join(vid_path, '{:s}_001_bbox.txt'.format(title)), 'w') as f:
#             f.writelines(box_list)
#     # save polygon
#     if len(polygon_list) > 0:
#         with open(os.path.join(vid_path, '{:s}_001.txt'.format(title)), 'w') as f:
#             f.writelines(polygon_list)
#     # save confidence
#     if len(confidence_list) > 0:
#         with open(os.path.join(vid_path, '{:s}_001_confidence.value'.format(title)), 'w') as f:
#             f.writelines(confidence_list)
#     # save time
#     if len(time_list) > 0:
#         with open(os.path.join(vid_path, '{:s}_time.value'.format(title)), 'w') as f:
#             f.writelines(time_list)
