import PIL
import tensorflow as tf
import hashlib
import io
import os
import untangle

if __name__ == '__main__':

    # dataset tools
    def int64_feature(values):
        """Returns a TF-Feature of int64s.
        Args:
          values: A scalar or list of values.
        Returns:
          a TF-Feature.
        """
        if not isinstance(values, (tuple, list)):
            values = [values]
        return tf.train.Feature(int64_list=tf.train.Int64List(value=values))


    def bytes_feature(values):
        """Returns a TF-Feature of bytes.
        Args:
          values: A string.
        Returns:
          a TF-Feature.
        """
        return tf.train.Feature(bytes_list=tf.train.BytesList(value=[values]))


    def float_list_feature(values):
        """Returns a TF-Feature of list of floats.
        Args:
          values: A float or list of floats.
        Returns:
          A TF-Feature.
        """
        return tf.train.Feature(float_list=tf.train.FloatList(value=values))


    def bytes_list_feature(values):
        """Returns a TF-Feature of list of bytes.
        Args:
          values: A string or list of strings.
        Returns:
          A TF-Feature.
        """
        return tf.train.Feature(bytes_list=tf.train.BytesList(value=values))


    def int64_list_feature(value):
        return tf.train.Feature(int64_list=tf.train.Int64List(value=value))


    def xml_to_tf_example(xml_obj):
        label_map_dict = {'bullseye':1}

        full_path = xml_obj.annotation.path.cdata
        filename = xml_obj.annotation.filename.cdata
        with tf.io.gfile.GFile(full_path, 'rb') as fid:
            encoded_jpg = fid.read()
        encoded_jpg_io = io.BytesIO(encoded_jpg)
        image = PIL.Image.open(encoded_jpg_io)
        if image.format != 'JPEG':
            raise ValueError('Image format not JPEG')
        key = hashlib.sha256(encoded_jpg).hexdigest()

        width = int(xml_obj.annotation.size.width.cdata)
        height = int(xml_obj.annotation.size.height.cdata)

        xmin = []
        ymin = []
        xmax = []
        ymax = []

        classes = []
        classes_text = []
        truncated = []

        for obj in xml_obj.annotation.object:
            xmin.append(float(obj.bndbox.xmin.cdata) / width)
            ymin.append(float(obj.bndbox.ymin.cdata) / height)
            xmax.append(float(obj.bndbox.xmax.cdata) / width)
            ymax.append(float(obj.bndbox.ymax.cdata) / height)
            classes_text.append(obj.name.cdata.encode('utf8'))
            classes.append(label_map_dict[obj.name.cdata])
            truncated.append(int(obj.truncated.cdata))

        example = tf.train.Example(features=tf.train.Features(feature={
            'image/height': int64_feature(height),
            'image/width': int64_feature(width),
            'image/filename': bytes_feature(filename.encode('utf8')),
            'image/source_id': bytes_feature(filename.encode('utf8')),
            'image/key/sha256': bytes_feature(key.encode('utf8')),
            'image/encoded': bytes_feature(encoded_jpg),
            'image/format': bytes_feature('jpeg'.encode('utf8')),
            'image/object/bbox/xmin': float_list_feature(xmin),
            'image/object/bbox/xmax': float_list_feature(xmax),
            'image/object/bbox/ymin': float_list_feature(ymin),
            'image/object/bbox/ymax': float_list_feature(ymax),
            'image/object/class/text': bytes_list_feature(classes_text),
            'image/object/class/label': int64_list_feature(classes),
            'image/object/truncated': int64_list_feature(truncated),
        }))
        return example

    data_dir = '/Users/z003z7n/Documents/AI2019/Tensorflow/TF2020/Project_bullseye/workspace/images/validate'
    tfrecord_path = '/Users/z003z7n/Documents/AI2019/Tensorflow/TF2020/Project_bullseye/workspace/data/validate.tfrecord'
    writer = tf.io.TFRecordWriter(tfrecord_path)
    annotations_dir = '/Users/z003z7n/Documents/AI2019/Tensorflow/TF2020/Project_bullseye/workspace/annotations/validate'
    examples_list = os.listdir(annotations_dir)
    for idx, example in enumerate(examples_list):
        if example.endswith('.xml'):
            path = os.path.join(annotations_dir, example)
            xml_obj = untangle.parse(path)
            tf_example = xml_to_tf_example(xml_obj)
            writer.write(tf_example.SerializeToString())
    writer.close()

