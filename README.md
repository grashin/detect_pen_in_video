# Detect pen in video


Алгоритм распознает ручку в виде объекта желтого цвета (может быть любой), далее определяет угол, на который повернута ручка относительно плоскости изображения и заключает этот объект в повернутый описанный прямоугольник.
Пример исходного изображения: ![image](/photos/yellow_2.jpg)

Пример получившегося изображения: ![image](/photos/pen_good_detect.png)

Маска в данном случае строится из предпроложения, что интересующий нас обьект желтого цвета, и при переводе изображения из RGB (red, green, blue) формата в HSV (hue, saturation, value), получаем: ![image](/photos/pen_detect_mask.png)

 **Используемые библиотеки**
* numpy 
* opencv
* yaml

***Используя коммандную строку:***

`pip install numpy opencv imutils`

---
##Использование


Image:
`python src/detect_pen_in_photo.py -i photos/yellow.jpg`

Video:
`python src/detect_pen_in_photo.py -v video/yellow_pen_1.mp4`




