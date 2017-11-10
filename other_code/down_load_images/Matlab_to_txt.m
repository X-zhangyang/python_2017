imgs = dir(['img-convert\','*.jpg']);
len = length(imgs);
fid = fopen('groundtruth.txt','w');
for i = 1:len
    imagename = imgs(i).name;
    image = imread(['img-convert\',imagename]);
    while 1
        [img,rect] = imcrop(image);
        rect = round(rect);
        label = input('please input lable:','s');
        fprintf(fid,'%s %s %d %d %d %d\n',imagename,label,rect(1),rect(2),rect(1)+rect(3),rect(2)+rect(4));
        isEnd = input('is this picture select over?','s');
        if isEnd=='s'
            break;
        end
    end
end
fclose(fid);