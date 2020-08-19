  
"""
Usage:
  # From tensorflow/models/
  # Create train data:
  python generate_tfrecord.py --csv_input=data/train_labels.csv  --image_dir="../"  --output_path=train.record
  # Create test data:
  python generate_tfrecord.py --csv_input=data/test_labels.csv   --image_dir="../"  --output_path=test.record
"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
import pandas as pd
import tensorflow as tf

from PIL import Image
from object_detection.utils import dataset_util
from collections import namedtuple, OrderedDict

flags = tf.compat.v1.flags

flags.DEFINE_string('csv_input', '', 'Path to the CSV input')
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
flags.DEFINE_string('image_dir', '', 'Path to images')
FLAGS = flags.FLAGS

# Import classes 
classes_image = {'rake': 74, 'can': 77, 'dustbin': 51, 'hoe': 73, 'spatula': 49, 'table': 3, 'mop': 84, 'radio': 63, 'microwave': 
30, 'air_onditioner': 64, 'vase': 61, 'broom': 53, 'jar': 76, 'candle': 54, 'switch': 85, 'tissue': 78, 'stove': 7, 'plunger': 23, 'lamp': 57, 'tray': 65, 'toothbrush': 4, 'floss': 17, 'bookshelf': 52, 'kitchen_scissors': 28, 'sellotape': 58, 'teapot': 2, 'bowl': 6, 'cup': 18, 'sink': 10, 'bathtub': 11, 'toilet_paper': 24, 'curtains': 62, 'whisk': 14, 'tongs': 80, 'jug': 8, 'fan': 42, 'faucet': 47, 'glove': 75, 'bottle_opener': 82, 'rolling_pin': 44, 'chopping_board': 68, 'razor': 79, 'bath_sponge': 12, 'pan': 16, 'grater': 66, 'scrub_brush': 5, 'clock': 21, 'kettle': 1, 'peeler': 67, 'rice_cooker': 41, 'telephone': 59, 'spoon': 43, 'toilet': 9, 'hanger': 83, 'lighter': 55, 'mirror': 26, 'sieve': 13, 'towel': 29, 'toothpaste': 27, 'television': 60, 'chair': 25, 'nail_clippers': 70, 'tweezer': 69, 'bucket': 50, 'iron': 56, 'lock': 71, 'plate': 20, 'fridge': 45, 'spade': 72, 'bottle': 15, 'soap': 48, 
'showerhead': 46, 'chopsticks': 22, 'straw': 81, 'knife': 19}
# TO-DO replace this with label map
def class_text_to_int(row_label):
        return classes_image[row_label]


def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def create_tf_example(group, path):
    with tf.compat.v1.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    filename = group.filename.encode('utf8')
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        xmins.append(row['xmin'] / width)
        xmaxs.append(row['xmax'] / width)
        ymins.append(row['ymin'] / height)
        ymaxs.append(row['ymax'] / height)
        classes_text.append(row['class'].encode('utf8'))
        classes.append(class_text_to_int(row['class']))

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example


def main(_):
    writer = tf.compat.v1.python_io.TFRecordWriter(FLAGS.output_path)
    path = os.path.join(FLAGS.image_dir)
    examples = pd.read_csv(FLAGS.csv_input)
    grouped = split(examples, 'filename')
    for group in grouped:
        tf_example = create_tf_example(group, path)
        writer.write(tf_example.SerializeToString())

    writer.close()
    output_path = os.path.join(os.getcwd(), FLAGS.output_path)
    print('Successfully created the TFRecords: {}'.format(output_path))


if __name__ == '__main__':
    tf.compat.v1.app.run()