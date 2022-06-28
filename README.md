![arc](https://github.com/cheneyjin/welding_dflux_subroutine/creoweld.png)
![result](https://github.com/cheneyjin/welding_dflux_subroutine/blob/main/result.png)
# WeldFlux
![weldFlux](https://img.shields.io/badge/cheneyjin-weldFlux1.6-brightgreen)  
This is a lightweight plug-in for abaqus to generate heat source subroutine DFLUX in welding and Additive Manufacturing modeling.

Watch a video tutorial at https://youtu.be/VQxh8XgLB2o https://www.bilibili.com/video/BV1bZ4y1U7Ho/

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
### Support straight, circular and **free (Pro-version) welding path**.
### The subroutine file uses mm-tonne-s units by default.




# WeldFlux
这是一个轻量级的abaqus插件程序，用于快速生成焊接热源子程序DFLUX。

视频教程 https://www.bilibili.com/video/BV1bZ4y1U7Ho/

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

### 支持直线型、圆弧型以及**任意自由焊接路径（仅高级版本）**。
### 子程序文件默认使用毫米-吨-秒单位制。
