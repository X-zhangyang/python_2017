function matlab_to_xml(mylabel)  
% ���ܣ���trainingImageLabel APP���ݸ�ʽ(table����)תΪVOC��ʽ��xml  
% ���룺 mylabelΪ�����������ռ�ı�ע�ļ�  
% ����� �Զ�����xmlSaveFolder�ļ��洢��ÿ��ͼ��Ӧһ��  
%  
% ˵����mylabel��ע����������command  
%  window����trainingImageLabeler��app�����ļ���ע����ע��󵼳���mylabel������Ȼ��ʹ�øú���  
% Example:  
%          matlab_to_xml(mylabel)  
%  
  
%%  
if nargin<1 || ~istable(mylabel)  
    error('�������̫�ٻ������ʹ�������trainingImageLabel APP������table�������ݣ�')  
    %     xmls_path = 'F:\imagesData\stopSignImages\*.xml';  
end  
  
%%  
tableLabel = mylabel; %�������Լ��ı�ע�õ�table��������  
variableNames = tableLabel.Properties.VariableNames; %cell����  
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
        database = annotation.createElement('database');%�ø��ڵ㽨��             
        database.appendChild(annotation.createTextNode('Unknow'));             
        source.appendChild(database);%���������ڵ�  
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
    for j = 2:numVariables %����ÿ������  
        ROI_matrix = rowTable.(variableNames{j});%cell  
%         ROI_matrix = ROI_matrix{:};  
        numROIS = size(ROI_matrix,1);  
        for ii = 1: numROIS % ����ÿ��ROI  
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