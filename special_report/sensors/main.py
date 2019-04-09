import ImgReceive as ImgRcv


ObjectA = ImgRcv.video2frame()

objectB_url = "https://192.168.43.1:8080/shot.jpg"
ObjectB = ImgRcv.IP_cam_get_image(objectB_url)

#objectC_url = " "
#ObjectC = ImgRcv.IP_cam_get_image(objectB_url)
