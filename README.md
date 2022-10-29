![arc](https://github.com/cheneyjin/welding_dflux_subroutine/blob/main/vs.png)
# WeldFlux
![weldFlux](https://img.shields.io/badge/cheneyjin-weldFlux1.6(trial)-brightgreen)  
This is a lightweight plug-in for abaqus to generate heat source subroutine DFLUX in welding and Additive Manufacturing modeling.

Watch a video tutorial (v1.5) at https://youtu.be/VQxh8XgLB2o https://www.bilibili.com/video/BV1bZ4y1U7Ho/

v1.6 for free path welding at https://www.bilibili.com/video/BV1Ve4y147ke/

v2.0-dve for 3D print at https://www.bilibili.com/video/BV1mT4y1z71p/    https://www.bilibili.com/video/BV13v4y1N7uA/

## install
Put the folder 'WeldFlux16' to abaqus_plugins directory.  
By default, it is located in %HOMEPATH%/abaqus_plugins in windows system.
## run
To run it, launch abaqus CAE, click plug-ins WeldFlux16 in manu bar.
## features
### The following heat source models are supported:
-  Planar Gauss
-  Double-ellipsoid
-  Cone body 

Support straight, circular and **free welding path(Pro-version).**

**The subroutine file uses mm-tonne-s units by default.**




# WeldFlux
这是一个轻量级的abaqus插件程序，用于快速生成焊接热源子程序DFLUX。

插件基础操作 https://www.bilibili.com/video/BV1bZ4y1U7Ho/ 

空间自由路径焊接  https://www.bilibili.com/video/BV1Ve4y147ke/

3D打印直线焊缝  https://www.bilibili.com/video/BV1mT4y1z71p/

3D打印弧形焊缝  https://www.bilibili.com/video/BV13v4y1N7uA/

## 安装
将'WeldFlux16'文件夹放于 abaqus_plugins 目录。
windows系统下一般位于%HOMEPATH%/abaqus_plugins
## 运行
启动abaqus CAE, 点击菜单栏中的plug-ins WeldFlux16运行。
## 特征
### 支持下列热源模型：
-  平面高斯
-  双椭球
-  圆锥体

支持直线型、圆弧型以及**任意自由焊接路径（仅高级版本）**。

子程序文件默认使用毫米-吨-秒单位制。
