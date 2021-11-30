python demo/top_down_img_demo_with_mmdet.py  \
   demo/mmdetection_cfg/faster_rcnn_r50_fpn_coco.py     https://download.openmmlab.com/mmdetection/v2.0/faster_rcnn/faster_rcnn_r50_fpn_1x_coco/faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth  \
   configs/body/2d_kpt_sview_rgb_img/topdown_heatmap/coco/res10_coco_192x192.py    work_dirs/res10_coco_192x192/epoch_100.pth     --img-root /mnt/data3/gyl/video_404/images/   \
    --img video000001.jpg     --out-img-root vis_results
#python demo/top_down_img_demo_with_mmdet.py     demo/mmdetection_cfg/faster_rcnn_r50_fpn_coco.py     https://download.openmmlab.com/mmdetection/v2.0/faster_rcnn/faster_rcnn_r50_fpn_1x_coco/faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth     configs/body/2d_kpt_sview_rgb_img/topdown_heatmap/coco/mobilenetv2_coco_256x192.py    https://download.openmmlab.com/mmpose/top_down/mobilenetv2/mobilenetv2_coco_256x192-d1e58e7b_20200727.pth     --img-root /mnt/data3/gyl/video_404/images/    --img video000001.jpg     --out-img-root vis_results

