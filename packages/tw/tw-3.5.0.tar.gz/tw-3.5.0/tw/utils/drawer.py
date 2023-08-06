# Copyright 2017 The KaiJIN Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Drawer based on OpenCV.

  - bounding box
  - lane
  - keypoints
  - heatmap
  - ...

  Each drawer could support two kind of input: numpy and torch.
  
  - numpy format use [H, W, C] format

"""
import numpy as np
import cv2
import pylab


def boundingbox(image, bboxes, labels=None, conf=0.0,
                bbox_thick=2,
                font_type=cv2.FONT_HERSHEY_SIMPLEX,
                font_thick=1,
                font_scale=0.4,
                **kwargs):
  """Render bounding box to image

  Args:
      image ([np.ndarray]): [H, W, C] uint8
      bboxes ([np.ndarray]): [N, 5(x1, y1, x2, y2, score(optional))] float
      labels (list[]]): [N, ]

  """
  assert isinstance(image, np.ndarray) and image.ndim == 3
  render = image.copy()

  # select score
  if bboxes.shape[1] == 5:
    scores = bboxes[:, 4]
  else:
    scores = None

  for i, bbox in enumerate(bboxes):

    # skip low confidence
    if scores is not None:
      if scores[i] < conf:
        continue

    # skip ignore labels

    # render bbox
    x1, y1, x2, y2 = bbox[:4]
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    cv2.rectangle(img=render,
                  pt1=(x1, y1),
                  pt2=(x2, y2),
                  color=(52, 213, 235),
                  thickness=bbox_thick)

    # render label
    if labels is not None:
      label = labels[i]
      if scores is not None:
        caption = '{}:{:.2f}'.format(label, scores[i])
      else:
        caption = '{}'.format(label)
      # get the width and height of the text box
      tw, th = cv2.getTextSize(text=caption,
                               fontFace=font_type,
                               fontScale=font_scale,
                               thickness=font_thick)[0]
      cv2.rectangle(render, (x1, y1), (x1 + tw + 2, y1 - th - 6), (52, 213, 235), cv2.FILLED)
      cv2.putText(render, caption, (x1, y1 - 4),
                  fontFace=font_type,
                  fontScale=font_scale,
                  color=[255, 255, 255],
                  thickness=font_thick)

  return render


def keypoints(image, points, **kwargs):
  """Draw points on image

  Args:
      image ([np.ndarray]): [H, W, C] uint8
      points ([np.ndarray]): [N, 2(x, y)] float

  """
  assert isinstance(image, np.ndarray) and image.ndim == 3
  assert isinstance(points, np.ndarray) and points.ndim == 2

  render = image.copy()
  radius = 5 if 'radius' not in kwargs else kwargs['radius']

  for _, (x, y) in enumerate(points):
    cv2.circle(render, (int(x), int(y)), radius=radius, color=(0, 255, 0), thickness=cv2.FILLED)

  return render
