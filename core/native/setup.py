#!/usr/bin/env python

import os
import sys
import glob
import importlib

from cx_Freeze import setup, Executable

_version = os.getenv('BUILD_COUNTER', '9')

base = None
if sys.platform == "win32":
  base = "Win32GUI"

# Need to copy all external files too.
external_dir = os.path.dirname(importlib.util.find_spec('external').origin)
external_resources = [f for f in glob.glob(os.path.join(external_dir, '*')) if f != '__init__.py' and f != '__pycache__']

print("sys.path", sys.path, file=sys.stderr)

setup(
    name="nao",
    version="0.1",
    description="Programming language for large scale computational networks",
    options={
      "build_exe": {
        "replace_paths": [("%s/" % p, "//") for p in sys.path],
        "bin_path_excludes": [
          "bazel-out/",
          *os.environ['CXFREEZE_BIN_PATH_EXCLUDES'].split(':'),
          sys.prefix,
        ],
        "bin_excludes": [
        ],
        "excludes": [
          "setuptools",
          "distutils",
        ],
        "includes": [
          "pkg_resources._vendor.packaging.version",
          "pkg_resources._vendor.packaging.specifiers",
          "pkg_resources._vendor.packaging.requirements",
          "pkg_resources._vendor.pyparsing",
          "numpy.core._methods",
          "numpy.lib.format",

          "tensorflow.contrib.framework.python.ops.gen_variable_ops",
          "tensorflow.contrib.layers.python.layers.utils",

        #   "tensorflow.contrib.cudnn_rnn.python.ops._cudnn_rnn_ops",
        #   "tensorflow.contrib.factorization.python.ops._clustering_ops",
        #   "tensorflow.contrib.factorization.python.ops._factorization_ops",
        #   "tensorflow.contrib.ffmpeg.ffmpeg",
        #   "tensorflow.contrib.framework.python.ops._variable_ops",
        #   "tensorflow.contrib.image.python.ops._image_ops",
        #   "tensorflow.contrib.input_pipeline.python.ops._input_pipeline_ops",
        #   "tensorflow.contrib.layers.python.ops._bucketization_op",
        #   "tensorflow.contrib.layers.python.ops._sparse_feature_cross_op",
        #   "tensorflow.contrib.nccl.python.ops._nccl_ops",
        #   "tensorflow.contrib.rnn.python.ops._gru_ops",
        #   "tensorflow.contrib.rnn.python.ops._lstm_ops",
        #   "tensorflow.contrib.tensor_forest.hybrid.python.ops._training_ops",
        #   "tensorflow.contrib.tensor_forest.python.ops._tensor_forest_ops",
          "tensorflow"
        ],
        "include_files": [
          *[(d, os.path.join("lib", "python3.5", "external", os.path.basename(d))) for d in external_resources]
        ],
        "packages": [
          "nao",
          "nao_parser",
        ]
      }
    },
    executables=[
      Executable(
          "%s/nao__init__.py" % os.path.dirname(__file__),
          base=base,
          initScript="%s/initscript.py" % os.path.realpath(os.path.dirname(__file__)),
          targetName="nao")
    ])
