

import numpy as np

global a 

def calculate_ROC(array_data,actual_issame, start, end, step):
    i = 0.01
    step_num = int((end-start)/step)
    temp_a = np.zeros((int((end-start)/step),2))
    if (len(array_data)==len(actual_issame)):
        for x in range (step_num):
            temp_a[(x-1),0],temp_a[(x-1),1],_=calculate_accuracy(start,array_data,actual_issame)
            start = start + step   
    else:
        print("Wrong intput")
    return temp_a
        

def calculate_accuracy(threshold, array_data, actual_issame):
    #predict_issame = np.less(array_data, threshold)
    predict_issame = np.greater(array_data, threshold)
#    print('calculate_accuracy %f' %threshold)
    tp = np.sum(np.logical_and(predict_issame, actual_issame))
    fp = np.sum(np.logical_and(predict_issame, np.logical_not(actual_issame)))
    tn = np.sum(np.logical_and(np.logical_not(predict_issame), np.logical_not(actual_issame)))
    fn = np.sum(np.logical_and(np.logical_not(predict_issame), actual_issame))
  
    tpr = 0 if (tp+fn==0) else float(tp) / float(tp+fn)
    fpr = 0 if (fp+tn==0) else float(fp) / float(fp+tn)
    acc = float(tp+tn)/array_data.size
    return tpr, fpr, acc
