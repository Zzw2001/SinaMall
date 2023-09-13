
# python manage.py shell
from goods.models import Carousel

carousels = [['https://cdn.cnbj1.fds.api.mi-img.com/mi-mall/81efb662f6c196595cd20a32c93978c5.jpeg?w=2452&h=920','2022年米粉节'],

['https://cdn.cnbj1.fds.api.mi-img.com/mi-mall/4b1f3d1bf1b9329ff2e7f398bafa8f84.jpg?thumb=1&w=1533&h=575&f=webp&q=90', ' Redmi K50 电竞版'],

 ['https://cdn.cnbj1.fds.api.mi-img.com/mi-mall/9e66e9d1e25726cc0dcb6b743e5b388b.png?thumb=1&w=1533&h=575&f=webp&q=90', 'Redmi MAX 100" 巨屏电视'],

 ['https://cdn.cnbj1.fds.api.mi-img.com/mi-mall/74a51ccb0237755ef3ad7021a6e6d43c.png?thumb=1&w=1533&h=575&f=webp&q=90', '米家新风空调']]

for i in carousels:
   Carousel.objects.create(imgPath=i[0], describes=i[1])