# DDos-attack-detection

## sdntopo.py
本次实验使用的拓扑，本次攻击针对的是h1

## train.py
模型训练的python程序

## model文件夹
用于保存训练后的模型

## tcpdump_start.sh
Ubuntu脚本文件，用于获取流量包

## 2.py
用于将获取的流表项转化为特征向量

## work.py
读取特征向量并判定端口流量是否异常

## 3.sh
Ubuntu脚本文件,用于按顺序执行tcpdump_start.sh、2.py、work.py，完成一次检测
