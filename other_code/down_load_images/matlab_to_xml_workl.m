function matlab_to_xml(mylabel)  
% 功能：把trainingImageLabel APP数据格式(table类型)转为VOC格式的xml  
% 输入： mylabel为导出到工作空间的标注文件  
% 输出： 自动生成xmlSaveFolder文件存储，每张图对应一个  
%  
% 说明：mylabel标注变量，请在command  
%  window输入trainingImageLabeler打开app进行文件标注，标注完后导出到mylabel变量，然后使用该函数  
% Example:  
%          matlab_to_xml(mylabel)  
%  
  
%%  
if nargin<1 || ~istable(mylabel)  
    error('输入参数太少或者类型错误！请用trainingImageLabel APP导出的table类型数据！')  
    %     xmls_path = 'F:\imagesData\stopSignImages\*.xml';  
end  
  
%%  
tableLabel = mylabel; %这里是自己的标注好的table类型数据  
variableNames = tableLabel.Properties.VariableNames; %cell类型  
numSamples = size(mylabel,1);  
numVariables = size(variableNames,2);  
  
%%  
for i = 1:numSamples  
    rowTable = tableLabel(i,:);  
    imageFullPathName = rowTable.(variableNames{1});%cell  
    addpath = char(imageFullPathName);  
    [pathstr,name,ext] = fileparts(addpath);  
    index =strfind(pathstr,'\');  
     
    annotation = com.mathworks.xml.XMLUtils.createDocument('annotation');  
    annotationRoot = annotation.getDocumentElement;  
         
    folder = annotation.createElement('folder');     
    folder.appendChild(annotation.createTextNode(pathstr(index(end)+1:end)));        
    annotationRoot.appendChild(folder);   
    %annotation.folder = pathstr(index(end)+1:end);  
    
    %annotation.filename = [name,ext];  
    filename = annotation.createElement('filename');     
    filename.appendChild(annotation.createTextNode([name,ext]));        
    annotationRoot.appendChild(filename);   

    
    %annotation.path = path;  
    path = annotation.createElement('path');      
    path.appendChild(annotation.createTextNode('D:\Learning\python\Download_Image\gun\100'));
    annotationRoot.appendChild(path);  
    
    source = annotation.createElement('source');  
    annotationRoot.appendChild(source); 
        database = annotation.createElement('database');%用根节点建立             
        database.appendChild(annotation.createTextNode('Unknow'));             
        source.appendChild(database);%依附到父节点  
        %annotation.source.database = 'Unknow';  
    
    image = imread(addpath);  
    
    size_ = annotation.createElement('size_');  
    annotationRoot.appendChild(size_);  
        width = annotation.createElement('width');  
        width.appendChild(annotation.createTextNode(num2str(size(image,2))));            
        size_.appendChild(width);%           
        height = annotation.createElement('height');           
        height.appendChild(annotation.createTextNode(num2str(size(image,1))));         
        size_.appendChild(height);%        
        depth = annotation.createElement('depth');       
        depth.appendChild(annotation.createTextNode(num2str(size(image,3))));   
        size_.appendChild(depth);%
%     annotation.size.width = size(image,2);  
%     annotation.size.height = size(image,1);  
%     annotation.size.depth = size(image,3); 
    
    segmented = annotation.createElement('segmented');  
    segmented.appendChild(annotation.createTextNode('0'));  
    annotationRoot.appendChild(segmented);  
    %annotation.segmented = 0;  
      
    objectnum = 0;  
    for j = 2:numVariables %对于每个变量  
        ROI_matrix = rowTable.(variableNames{j});%cell  
%         ROI_matrix = ROI_matrix{:};  
        numROIS = size(ROI_matrix,1);  
        for ii = 1: numROIS % 对于每个ROI  
            %             field = ['object',num2str(ii)];  
            objectnum= objectnum+1;  
            object = annotation.createElement('object');
            annotationRoot.appendChild(object);
                name_obj = annotation.createElement('name');
                name_obj.appendChild(annotation.createTextNode(variableNames{1,j}));
                object.appendChild(name_obj);%
                pose = annotation.createElement('pose');
                pose.appendChild(annotation.createTextNode('Unspecified'));
                object.appendChild(pose);%
                truncated = annotation.createElement('truncated');
                truncated.appendChild(annotation.createTextNode('0'));
                object.appendChild(truncated);%
                difficult = annotation.createElement('difficult');
                difficult.appendChild(annotation.createTextNode('0'));
                object.appendChild(difficult);%
                bndbox = annotation.createElement('bndbox');
                object.appendChild(bndbox);%
                    xmin = annotation.createElement('xmin');
                    xmin.appendChild(annotation.createTextNode(num2str(ROI_matrix(ii,1))));
                    bndbox.appendChild(xmin);%
                    ymin = annotation.createElement('ymin');
                    ymin.appendChild(annotation.createTextNode(num2str(ROI_matrix(ii,2))));
                    bndbox.appendChild(ymin);%
                    xmax = annotation.createElement('xmax');
                    xmax.appendChild(annotation.createTextNode(num2str(ROI_matrix(ii,3))));
                    bndbox.appendChild(xmax);%
                    ymax = annotation.createElement('ymax');
                    ymax.appendChild(annotation.createTextNode(num2str(ROI_matrix(ii,4))));
                    bndbox.appendChild(ymax);%
        end  
    end
      
    if ~exist('xmlSaveFolder','file')  
        mkdir xmlSaveFolder  
    end  
    xmlwrite(['xmlSaveFolder\',name,'.xml'],annotation);  
    clear annotation; 
end  