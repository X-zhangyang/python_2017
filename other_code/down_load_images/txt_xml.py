#encoding=utf-8
 
import sys
import os
import codecs
import cv2 


#注意：训练不同种类时，需要修改line   xml.write('\t\t<name>类型</name>\n')

root = r'D:\\Learning\\python\\Download_Image\\revise_images\\Annotations\\'  #存放地址
fp = open('D:\\Learning\\python\\Download_Image\\revise_images\\raccoon.txt') #shur 
fp2 = open('train.txt', 'w')
uavinfo = fp.readlines()
 
for i in range(len(uavinfo)):
    line = uavinfo[i]
    line = line.strip().split('\t')   
    img =cv2.imread(line[0])
    sp = img.shape
    height = sp[0]
    width = sp[1]
    depth = sp[2]
    info1 = line[0].split('\\')[-1]
    info2 = info1.split('.')[0]
 
    l_pos1 = line[1]
    l_pos2 = line[2]
    r_pos1 = line[3]
    r_pos2 = line[4]
    fp2.writelines(info2 + '\n')
    with codecs.open(root +r'\\'+ info2 + '.xml', 'w', 'utf-8') as xml:
        xml.write('<annotation>\n')
        xml.write('\t<folder>VOC2012</folder>\n')
        xml.write('\t<filename>' + info1 + '</filename>\n')
        xml.write('\t<source>\n')
        xml.write('\t\t<database>Myo own Database</database>\n')
        xml.write('\t\t<annotation>PASCAL VOC2012</annotation>\n')
        xml.write('\t\t<image>flickr</image>\n')
        xml.write('\t</source>\n')
        xml.write('\t<size>\n')
        xml.write('\t\t<width>'+ str(width) + '</width>\n')
        xml.write('\t\t<height>'+ str(height) + '</height>\n')
        xml.write('\t\t<depth>' + str(depth) + '</depth>\n')
        xml.write('\t</size>\n')
        xml.write('\t\t<segmented>0</segmented>\n')
        xml.write('\t<object>\n')
        xml.write('\t\t<name>raccoon</name>\n')
        xml.write('\t\t<pose>Unspecified</pose>\n')
        xml.write('\t\t<truncated>0</truncated>\n')
        xml.write('\t\t<difficult>0</difficult>\n')
        xml.write('\t\t<bndbox>\n')
        xml.write('\t\t\t<xmin>' + l_pos1 + '</xmin>\n')
        xml.write('\t\t\t<ymin>' + l_pos2 + '</ymin>\n')
        xml.write('\t\t\t<xmax>' + r_pos1 + '</xmax>\n')
        xml.write('\t\t\t<ymax>' + r_pos2 + '</ymax>\n')
        xml.write('\t\t</bndbox>\n')
        xml.write('\t</object>\n')
        xml.write('</annotation>')
fp2.close()




''' 
<annotation>
	<folder>VOC2012</folder>                           
	<filename>2007_000392.jpg</filename>                               //文件名
	<source>                                                           //图像来源（不重要）
		<database>The VOC2007 Database</database>
		<annotation>PASCAL VOC2007</annotation>
		<image>flickr</image>
	</source>
	<size>					                           //图像尺寸（长宽以及通道数）						
		<width>500</width>
		<height>332</height>
		<depth>3</depth>
	</size>
	<segmented>0</segmented>		                           //是否用于分割（在图像物体识别中01无所谓）
	<object>                                                           //检测到的物体
		<name>horse</name>                                         //物体类别
		<pose>Right</pose>                                         //拍摄角度
		<truncated>0</truncated>                                   //是否被截断（0表示完整）
		<difficult>0</difficult>                                   //目标是否难以识别（0表示容易识别）
		<bndbox>                                                   //bounding-box（包含左下角和右上角xy坐标）
			<xmin>100</xmin>
			<ymin>96</ymin>
			<xmax>355</xmax>
			<ymax>324</ymax>
		</bndbox>
	</object>
	<object>                                                           //检测到多个物体
		<name>person</name>
		<pose>Unspecified</pose>
		<truncated>0</truncated>
		<difficult>0</difficult>
		<bndbox>
			<xmin>198</xmin>
			<ymin>58</ymin>
			<xmax>286</xmax>
			<ymax>197</ymax>
		</bndbox>
	</object>
</annotation>



'''
