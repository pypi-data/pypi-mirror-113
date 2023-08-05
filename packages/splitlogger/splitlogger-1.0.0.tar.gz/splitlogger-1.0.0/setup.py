from setuptools import find_packages, setup

name = 'splitlogger'

setup(
    name=name,  # 包名同工程名，这样导入包的时候更有对应性
    version='1.0.0',
    author="Jayson",
    author_email='jaysonteng@163.com',
    description="encapsulate logger",
    python_requires="==3.7.*",
    packages=find_packages(),
    package_data={"": ["*"]},  # 数据文件全部打包
    include_package_data=True,  # 自动包含受版本控制(svn/git)的数据文件
    zip_safe=False,
)


"""
# test
import numpy as np
import cv2
from img_classifier.detect_main import Mainclassifier
frame = cv2.imdecode(np.fromfile('王源国旗.jpg', dtype=np.uint8), 1)
classifier = Mainclassifier(device='0')
model_names = classifier.choose_models()
rt = classifier.img_detect(frame, model_names)
"""
