# Copyright (c) OpenMMLab. All rights reserved.
import os
import warnings
from argparse import ArgumentParser

from mmpose.apis import (inference_top_down_pose_model, init_pose_model,
                         process_mmdet_results, vis_pose_result)
from mmpose.datasets import DatasetInfo
import torch

try:
    from mmdet.apis import inference_detector, init_detector
    has_mmdet = True
except (ImportError, ModuleNotFoundError):
    has_mmdet = False


def main():
    """Visualize the demo images.

    Using mmdet to detect the human.
    """
    parser = ArgumentParser()
    parser.add_argument('det_config', help='Config file for detection')
    parser.add_argument('det_checkpoint', help='Checkpoint file for detection')
    parser.add_argument('pose_config', help='Config file for pose')
    parser.add_argument('pose_checkpoint', help='Checkpoint file for pose')
    parser.add_argument('--img-root', type=str, default='', help='Image root')
    parser.add_argument('--img', type=str, default='', help='Image file')
    parser.add_argument(
        '--show',
        action='store_true',
        default=False,
        help='whether to show img')
    parser.add_argument(
        '--out-img-root',
        type=str,
        default='',
        help='root of the output img file. '
        'Default not saving the visualization images.')
    parser.add_argument(
        '--device', default='cuda:0', help='Device used for inference')
    parser.add_argument(
        '--det-cat-id',
        type=int,
        default=1,
        help='Category id for bounding box detection model')
    parser.add_argument(
        '--bbox-thr',
        type=float,
        default=0.3,
        help='Bounding box score threshold')
    parser.add_argument(
        '--kpt-thr', type=float, default=0.3, help='Keypoint score threshold')
    parser.add_argument(
        '--radius',
        type=int,
        default=4,
        help='Keypoint radius for visualization')
    parser.add_argument(
        '--thickness',
        type=int,
        default=1,
        help='Link thickness for visualization')

    assert has_mmdet, 'Please install mmdet to run the demo.'

    args = parser.parse_args()

    assert args.show or (args.out_img_root != '')
    assert args.img != ''
    assert args.det_config is not None
    assert args.det_checkpoint is not None

    det_model = init_detector(
        args.det_config, args.det_checkpoint, device=args.device.lower())

    # build the pose model from a config file and a checkpoint file
    export = False

    pose_model = init_pose_model(
        args.pose_config, args.pose_checkpoint, device=args.device.lower())
    if export is True:
        pose_model.eval()
        #input_shape = (1,3,320, 576)
        input_shape = (1,3,192, 192)

        #input_array = torch.from_numpy(np.load("input.npy"))
        #a = model(input_array)
        #for i in a:
        #  print(i.mean())
        torch.jit.trace(pose_model.cpu(), torch.rand(input_shape),).save('pose_192_resnet10.pth')
        return


    dataset = pose_model.cfg.data['test']['type']
    dataset_info = pose_model.cfg.data['test'].get('dataset_info', None)
    if dataset_info is None:
        warnings.warn(
            'Please set `dataset_info` in the config.'
            'Check https://github.com/open-mmlab/mmpose/pull/663 for details.',
            DeprecationWarning)
    else:
        dataset_info = DatasetInfo(dataset_info)
    import cv2
    import numpy as np
    import glob
    import tqdm
    image_name_list = glob.glob("ActionDataset-1125/*/*/*/*.jpg")
    for image_name in tqdm.tqdm(image_name_list):

        img = cv2.imread(image_name)

        # test a single image, the resulting box is (x1, y1, x2, y2)
        #mmdet_results = inference_detector(det_model, image_name)
        x1,y1,x2,y2 = 0,0,img.shape[1]-1,img.shape[0]-1

        # keep the person class bounding boxes.
        #person_results = process_mmdet_results(mmdet_results, args.det_cat_id)
        person_results = [{'bbox': np.array([x1,y1,x2,y2,1.0])}]
        # test a single image, with a list of bboxes.

        # optional
        return_heatmap = False

        # e.g. use ('backbone', ) to return backbone feature
        output_layer_names = None

        pose_results, returned_outputs = inference_top_down_pose_model(
            pose_model,
            image_name,
            person_results,
            bbox_thr=args.bbox_thr,
            format='xyxy',
            dataset=dataset,
            dataset_info=dataset_info,
            return_heatmap=return_heatmap,
            outputs=output_layer_names)
        
        
        outpath = os.path.join("npy_out",image_name.replace(".jpg", ".npy"))
        outdir = "/".join(outpath.split("/")[:-1])
        os.makedirs(outdir, exist_ok=True)
        np.save(os.path.join("npy_out",image_name.replace(".jpg", ".npy")),pose_results[0]["keypoints"])
        # if args.out_img_root == '':
        #     out_file = None
        # else:
        #     os.makedirs(args.out_img_root, exist_ok=True)
        #     out_file = os.path.join(args.out_img_root, image_name)

        # show the results
        # vis_pose_result(
        #     pose_model,
        #     image_name,
        #     pose_results,
        #     dataset=dataset,
        #     dataset_info=dataset_info,
        #     kpt_score_thr=args.kpt_thr,
        #     radius=args.radius,
        #     thickness=args.thickness,
        #     show=args.show,
        #     out_file=out_file)


if __name__ == '__main__':
    main()
