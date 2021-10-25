import numpy as np
import math



# 目标图像在原图对应的几何坐标位置,输出对应位置的几何坐标
def ge_ce(ssize,dsize):
    '''
    get the Absolute location in sorce loaction
    '''    
    result=np.zeros([dsize[0],dsize[1],2])
    for i in range(dsize[0]):   
        for j in range(dsize[1]):
            # SrcX=(i+0.5)* (ssize[0]/dsize[0]) -0.5
            # SrcY=(j+0.5)*(ssize[1]/dsize[1])-0.5
            SrcX=(i+1)* (ssize[0]/(dsize[0]+1)) -0.5
            SrcY=(j+1)*(ssize[1]/(dsize[1]+1))-0.5
            result[i][j]=[SrcX,SrcY]

    # 对应（0，0）在图片左上角
    # y,x,c[x,y]
    return result


def single_biline(x,x0,x1,y0p,y1p):
    # w1=(x-x0)/(x1-x0)
    # w2=(x1-x)/(x1-x0)
    # 设 alpha=w1
    # 原理和注释一样，因为像素默认长度为1，所以x1-x0一定为1
    # 使用alpha避免负数的问题
    alpha=abs(x-x0)
    y=alpha*y0p+(1-alpha)*y1p

    return y

def double_biline(image,ssize,dsize):
    '''
    image: cvform [h,w]
    SSIZE: The size of Source image [h,w]
    DSIZE: The size of Destination image [h,w]
    '''
    result=np.zeros(dsize,dtype=np.uint8)
    ssize=np.array(ssize)
    gece=ge_ce(ssize,dsize)
    # print(gece)
    for i in range(dsize[0]):
        for j in range(dsize[1]):
            # 边界溢出处理
            if gece[i][j][0]<0:
                gece[i][j][0]=0
            if gece[i][j][0]>(ssize[0]-1):
                gece[i][j][0]=ssize[0]-1
             
            if gece[i][j][1]<0:
                gece[i][j][1]=0
            if gece[i][j][1]>(ssize[1]-1):
                gece[i][j][1]=ssize[1]-1
            # print(gece[i][j])

            x0= int(math.floor(gece[i][j][0]))
            x1= int(math.ceil(gece[i][j][0]))
            y0= int(math.floor(gece[i][j][1]))
            y1= int(math.ceil(gece[i][j][1]))

                
            y0p=image[x0][y0]
            y1p=image[x1][y0]
            y2p=image[x0][y1]
            y3p=image[x1][y1]

            p1=single_biline(gece[i][j][0],x0,x1,y0p,y1p)
            p2=single_biline(gece[i][j][0],x0,x1,y2p,y3p)
            p3=single_biline(gece[i][j][1],y0,y1,p1,p2)
            result[i][j]=np.array(p3,dtype=np.uint8)


    return result



if __name__=="__main__":
    image=[[232,233,215,157],
        [234,235,157,55],
        [26,156,133,7],
        [159,27,45,84]]
    # image=np.random.randint(0, 255, (200, 300), dtype=np.uint8)
    image=np.array(image)
    print(image.shape)


    # length,width
    SSIZE=image.shape
    DSIZE=[2,2]


    image=double_biline(image,SSIZE,DSIZE)
    print(image)

