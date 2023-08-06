#!/usr/bin/env python
# coding: utf-8

# In[11]:


import glob
from PIL import Image

class GifConverter:
    def __init__(self, path_in=None, path_out=None, resize=(320,240)):
        """
        path_in : 원본 여러 이미지 경로(Ex : images/*.png)
        path_out : 결과 이미지 경로(Ex : output/filename.gif)
        resize : 리사이징 크기(Ex : (320,240))
        """
        self.path_in = path_in or './*.png'
        self.path_out = path_out or './output.gif'
        self.resize = resize
        
    def convert_gif(self):
        """
        GIF 이미지 변환 기능 수행
        """
        print(self.path_in, self.path_out, self.resize)
        img, *images =         [Image.open(f).resize(self.resize) for f in sorted(glob.glob(self.path_in))]
        try:
            img.save(
                fp = self.path_out,
                format='GIF',
                append_images=images,
                save_all=True,
                duration=100,
                loop=1
            )
        except IOError:
            print('Cannot convert!', img)

# 이 부분은 from .. import.. 로 할시 실행되지 않는다!!!!!
if __name__ == '__main__':
    # 클래스 
    c = GifConverter('./project/images/*.png', './project/image_out/result.gif', (320,240))

    # 변환
    c.convert_gif()
    print(GifConverter.__init__.__doc__)

