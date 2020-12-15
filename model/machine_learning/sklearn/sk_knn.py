# -*- coding: utf-8 -*-
# @File:       |   sk_knn.py 
# @Date:       |   2020/12/14 10:22
# @Author:     |   ThinkPad
# @Desc:       |  
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV


def kNN_iris_gscv():
    """
    用kNN对鸢尾花进行分类,添加网格搜索和交叉验证
    :return:
 """
    # 1.获取数据
    iris = load_iris()
    # 2.划分数据集
    x_train, x_test, y_train, y_test = train_test_split(iris.data, iris.target, random_state=1)
    # 3.特征工程：标准化
    transfer = StandardScaler()
    print(x_train)
    x_train = transfer.fit_transform(x_train)
    x_test = transfer.transform(x_test)  # 使用训练集的平均值和标准差
    print(x_train)
    # 4.模型训练
    estimator = KNeighborsClassifier()
    # 加入网格搜索和交叉验证
    # 参数准备
    param_dict = {"n_neighbors": [1, 3, 5, 7, 9, 11]}
    estimator = GridSearchCV(estimator, param_grid=param_dict, cv=10)  # 对estimator预估器进行10折交叉验证
    estimator.fit(x_train, y_train)  # 模型拟合
    # 5.模型评估
    # 方法1：比对真实值和预测值
    y_predict = estimator.predict(x_test)
    print(y_predict)
    print("直接比对真实值和预测值:\n", y_predict == y_test)
    # 方法2：直接计算准确率
    score = estimator.score(x_test, y_test)
    print("准确率为:", score)

    # 最佳参数:best_params
    print("最佳参数:\n", estimator.best_params_)
    # 最佳结果:best_score_
    print("最佳结果:\n", estimator.best_score_)
    # 最佳估计器:best_estimator_
    print("最佳估计器:\n", estimator.best_estimator_)
    # 交叉验证结果:cv_results_
    print("交叉验证结果:\n", estimator.cv_results_)
    return None


if __name__ == "__main__":
    kNN_iris_gscv()
