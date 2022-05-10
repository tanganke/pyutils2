# See Also:
# - https://scikit-learn.org/stable/modules/classes.html#module-sklearn.metrics
import math
import numpy as np

# ---------------------------------------------------
#               Binary Classification
#
#                   实                    际
# ----------------------------------------------------
#          |        1           |            0
# ----------------------------------------------------
# 预 |  1  |  TP（True Positive）|   FP（False Positive）
#     ------------------------------------------------
# 测 |  0  | FN（False Negative）|   TN（True Negative）
# ----------------------------------------------------


def binary_precision(tp: float, fp: float) -> float:
    """
    计算二分类的精确率,即为预测为A的数据中，真实值为A的比例.
    precision度量的是「查准率」，在所有检测出的正样本中是不是实际都为正样本。
    比如在垃圾邮件判断等场景中，要求有更高的precision，确保放到回收站的都是垃圾邮件。
    """
    return tp / (tp + fp)


def binary_recall(tp: float, fn: float) -> float:
    """
    计算二分类的召回率,即为在所有的真实值为A的数据中，预测为A的比例。
    recall度量的是「查全率」，所有的正样本是不是都被检测出来了。
    比如在肿瘤预测场景中，要求模型有更高的recall，不能放过每一个肿瘤。
    """
    return tp / (tp + fn)


def binary_accuracy(tp: float, fp: float, fn: float, tn: float) -> float:
    """
    计算二分类的准确率
    """
    return (tp + tn) / (tp + fp + fn + tn)



