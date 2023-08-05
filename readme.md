# Introdution to Project

这个项目是用来将MediaPipe的预测结果转换成指定格式的json，以便于用于数据集的形成和其他模型的训练。

---

## Folder Structure

整个项目的文件夹结构解释如下：

```
├─model
├─data
├─dataset
├─mediapipe
├─labelme
├─utils
   ├─__init__.py
   ├─mediapipe2data.py
   ├─labelme2data.py
├─demo.ipynb
├─visualize.ipynb
└─readme.md
```

1. data文件夹存放测试图片
2. dataset文件夹存放整合好的数据集json文件
3. model文件夹存放MediaPipe测试模型
4. mediapipe存放mediapipe的输出
5. labelme存放labelme的输出
6. demo.ipynb展示
7. visualize.ipynb展示了怎么对一个文件夹的图片进行可视化

---

## The Content of Json File

`image_id`：一个Json文件对应着一张图片，也即一个对应的 `image_id`。

 `image_info`保存着对应图片的宽 `w`，高 `h`信息。

`keypoints`保存每只手的关键点信息，具体内容如下所示：

* `hand_keypoints`保存关键点的坐标 `<x,y>`。注意此处的坐标是归一化之后的坐标，以像素为单位。
* `hand_score`中是手的置信度。
* `hand_type`标志着是左手 `Left`还是右手 `Right`。

  ![1690979196634](.readme/1690979196634.png)
