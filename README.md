![arc](https://github.com/cheneyjin/welding_dflux_subroutine/blob/main/vs.png)
# Abaqus WeldToolkit Overview
It is a collection of abaqus plug-ins for facilitating welding and Additive Manufacturing modeling.
- **WeldFlux:** to generate heat source subroutine DFLUX in welding modeling.
- **AMFlux:** Additive Manufacturing modeling.
- **WeldGeom:** to build weld geometry especially multipass weld geometry.
- **AutoRot:** to rotate model automaticly in CAE.
- **ThermoToMech:** to transform a thermal analysis job(.inp) to a mechnical one in sequential thermomechanical calculation.
- **Convert units:** to convert units used in thermomechanical calculation.

# WeldFlux Changelog
![weldFlux](https://img.shields.io/badge/cheneyjin-weldFlux1.6.1-brightgreen)  
This is a lightweight plug-in for abaqus to generate heat source subroutine DFLUX in welding and Additive Manufacturing modeling.

Watch videos tutorial (v1.5) at https://youtu.be/VQxh8XgLB2o https://www.bilibili.com/video/BV1bZ4y1U7Ho/

v1.6 for free path welding at https://www.bilibili.com/video/BV1Ve4y147ke/

v1.6.1 pulse/CMT welding at https://www.bilibili.com/video/BV1LK411R77m/

v1.7.0 swing welding at https://www.bilibili.com/video/BV11A411C7mw/

v1.7.1 support for multi-pass welding at https://www.bilibili.com/video/BV1hT411n7WU/

v1.7.2 a private version for AM simulation

v1.7.3 support for multi sources and hybrid welding at https://www.bilibili.com/video/BV1uK411v7AX/

v2.0-dve for 3D print at https://www.bilibili.com/video/BV1mT4y1z71p/    https://www.bilibili.com/video/BV13v4y1N7uA/    
now it is named AMFlux1.0 (avtivate element by Model Change). 
Ask author for a new 3D print plugin EventGenerator1.1 (activate element by Event Series) at https://www.bilibili.com/video/BV1sV4y1y7Pt/

v1.8.0 support for FSW sources at https://www.bilibili.com/video/BV1dUW3eGEFD

v1.8.1 support for segmented sources at https://www.bilibili.com/video/BV16m2tYqET6/

v1.8.2 support for CW/CCW swing welding.

# WeldGeom
This plugin is used to create weld geometry especially multipass weld geometry in abaqus.
Watch videos tutorial (v1.0) at https://www.bilibili.com/video/BV1M84y1g7Jd/

## install
Put the folder 'WeldFlux161' to abaqus_plugins directory.  
By default, it is located in %HOMEPATH%/abaqus_plugins in windows system.
## run
To run it, launch abaqus CAE, click plug-ins WeldFlux161 in manu bar.
## features
### The following heat source models are supported:
-  Planar Gauss
-  Double-ellipsoid
-  Cone body 

Support straight, circular and **free welding path(Pro-version).**

**The subroutine file uses mm-tonne-s units by default.**

# Abaqus焊接工具箱简介
这是一系列abaqus插件合集，用来为焊接及增材制造模拟提供方便。
- WeldFlux: 在焊接及增材制造模拟中生成热源子程序DFLUX。
- AMFlux: 增材制造模拟。
- WeldGeom: 建立焊缝几何，尤其是多道焊几何模型。
- AutoRot: 在CAE中自动旋转模型。
- ThermoToMech: 在顺序热力耦合计算中，将热场计算文件（inp）转换为后续的力场计算文件。
- Convert units: 用于大多数热力计算中的单位转换。

# WeldFlux更新历史
这是一个轻量级的abaqus插件程序，用于快速生成焊接热源子程序DFLUX。

插件基础操作 (v1.5) https://www.bilibili.com/video/BV1bZ4y1U7Ho/ 

空间自由路径焊接 (v1.6) https://www.bilibili.com/video/BV1Ve4y147ke/

3D打印直线焊缝  (v2.0-dev) https://www.bilibili.com/video/BV1mT4y1z71p/

3D打印弧形焊缝 (v2.0-dev) https://www.bilibili.com/video/BV13v4y1N7uA/    
现命名为AMFlux

脉冲焊及CMT焊接 (v1.6.1) https://www.bilibili.com/video/BV1LK411R77m/

摆动焊接 (v1.7.0) https://www.bilibili.com/video/BV11A411C7mw/

支持多道焊（v1.7.1）https://www.bilibili.com/video/BV1hT411n7WU/

支持增材制造中热源自动接续(v1.7.2)  这是一个私人版本

支持多热源和复合热源(v1.7.3) https://www.bilibili.com/video/BV1uK411v7AX/

支持搅拌摩擦焊热源(v1.8.0) https://www.bilibili.com/video/BV1dUW3eGEFD

支持分段热源(v1.8.1) https://www.bilibili.com/video/BV16m2tYqET6/

支持螺旋摆动热源(v1.8.2).


## 安装
将'WeldFlux161'文件夹放于 abaqus_plugins 目录。
windows系统下一般位于%HOMEPATH%/abaqus_plugins
## 运行
启动abaqus CAE, 点击菜单栏中的plug-ins WeldFlux161运行。
## 特征
### 支持下列热源模型：
-  平面高斯
-  双椭球
-  圆锥体

支持直线型、圆弧型以及**任意自由焊接路径（仅高级版本）**。

子程序文件默认使用毫米-吨-秒单位制。
