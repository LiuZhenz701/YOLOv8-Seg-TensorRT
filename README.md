# YoloV8-segmentation with TensorRT on Ubuntu

Yolov8 segmentation custom dataset train and boost with TensorRT
- TensorRT implementation see [cyrusbehr](https://github.com/cyrusbehr/YOLOv8-TensorRT-CPP)
- Finds codes in `/scripts`
- My own result in `/run/segment`
- [Demo (Youtube)](https://youtu.be/hgp1QCzv4Lo)
- [Demo (Bilibili)](https://www.bilibili.com/video/BV1nQVYesEvy/?share_source=copy_web&vd_source=ed5dd912a49925c5664ba9d64e3d058c)


## **Prerequisites**
1. **CUDA (Ver. 12.1)**
  - installation follows:
    [CUDA 12.1 Download](https://developer.nvidia.com/cuda-12-1-0-download-archive?target_os=Linux&tsarget_arch=x86_64&Distribution=Ubuntu&target_version=20.04&target_type=deb_local)
    - **MUST USE LOCAL INSTALL**
      - `wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin`
      - `sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/`
      - `cuda-repository-pin-600`
      - `wget https://developer.download.nvidia.com/compute/cuda/12.1.0/local_installers/cuda-repo-ubuntu2004-12-1-local_12.1.0-530.30.02-1_amd64.deb`
      - `sudo dpkg -i cuda-repo-ubuntu2004-12-1-local_12.1.0-530.30.02-1_amd64.deb`
      - `sudo cp /var/cuda-repo-ubuntu2004-12-1-local/cuda-*-keyring.gpg /usr/share/keyrings/`
      - `sudo apt-get update`
      - `sudo apt-get -y install cuda`

2. **cuDNN (Ver. 8.9.7)**
  - installation follows:
    [cuDNN 8.9.7 Download](https://developer.nvidia.com/rdp/cudnn-archive)
      - Select **Download cuDNN v8.9.7 (December 5th, 2023), for CUDA 12.x**
      - Run commands below:
        - `tar -xvf cudnn-linux-x86_64-8.9.7.29_cuda12-archive.tar.xz`
        - `sudo cp cudnn-*-archive/include/cudnn*.h /usr/local/cuda/include`
        - `sudo cp -P cudnn-*-archive/lib/libcudnn* /usr/local/cuda/lib64`
        - `sudo chmod a+r /usr/local/cuda/include/cudnn.h /usr/local/cuda/lib64/libcudnn*`

3. **OpenCV_with CUDA & cuDNN (Ver. 4.9.0)**
  - installation follows:
    - **NOTE THAT THIS IS THE ONLY WAY WORKS ON MY PC, IT MAY NOT BE 100% CORRECT.**  
    **IF YOU HAVE INSTALLED CORRECTLY BEFORE, DO NOT FOLLOW THIS INSTRUCTION**
        - `sudo apt install build-essential`
        - `sudo apt install python3-pip`
        - `pip3 install cmake`
        - `git clone https://github.com/opencv/opencv.git`
        - `git clone https://github.com/opencv/opencv_contrib.git`
        - `cd opencv`
        - `mkdir build`
        - `chmod +x my_build_opencv.sh`
        - `./ my_build_opencv.sh`  
    **NOTE: CHANGE `-D CUDA_ARCH_BIN=8.6` IN `my_build_opencv` TO THE CORRECT VERSION FOR YOUR GPU**


4. **TensorRT (Ver. 10.0.1)**
    - installation follows:
    [TensorRT 10.x Download](https://developer.nvidia.com/tensorrt)
      - **MUST CLICK ON *GET STARTED* THEN *DOWNLOAD NOW***
      - Run commands below:
        - `tar -xzvf TensorRT-10.0.1.6.Linux.x86_64-gnu.cuda-12.4.tar.gz`
        - `export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/mnt/d/WSL/library/TensorRT-10.0.1.6/lib`
        - `cd TensorRT-10.0.1.6/python`
       - `python3 -m pip install tensorrt-10.0.1-cp38-none-linux_x86_64.whl`  
    **NOTE: CHANGE THE VERSION WITH YOUR TENSORRT VERSION & PYTHON VERSION**
        - `cd TensorRT-10.0.1.6/onnx_graphsurgeon`
        - `python3 -m pip install onnx_graphsurgeon-0.5.0-py2.py3-none-any.whl`

5. **YOLOv8-TensorRT-CPP Github Repo**
  - instruction:
  [Github Link](https://github.com/cyrusbehr/YOLOv8-TensorRT-CPP?tab=readme-ov-file)
    - `git clone https://github.com/cyrusbehr/YOLOv8-TensorRT-CPP --recursive`
    - `cd YOLOv8-TensorRT-CPP`
    - `mkdir build`
    - `cd build`
    - `cmake ..`
    - `make -j`

6. **Image Library**
  - We use [RELLIS-3D](https://github.com/unmannedlab/RELLIS-3D) as our image library.
  - `Raw image` and `Color Annotated Image` folders can be downloaded through [Google Drive](https://drive.google.com/file/d/1F3Leu0H_m6aPVpZITragfreO_SGtL2yV/view?pli=1) or [BaiduDisk](https://pan.baidu.com/s/1akqSm7mpIMyUJhn_qwg3-w?pwd=4gk3) (提取码：`4gk3`)
  - Also download `ontology.csv`

## **INSTRUCTION**
**PLEASE READ ALL FOUR `.py` FILES FIRST**
  1. **Train Yolov8-seg Model**
      - After downloading all the images we need, change the paths in `ConvertImgToLabel.py`, `DeleteFile.py`, `InstanceSegmentation.py` to the location to your image folder and ontology file
      - Use `DeleteFile.py` to delete useless raw images, since some raw images do not have corresponding color annotation
      - Run `ConvertImgToLabel.py` to generate YOLOv8 format .txt labels for your images
      - Run `InstanceSegmentation.py` to train the model (you can choose to train with best.pt)
      - Check the results in `runs/segment/train`, if the result looks good, go to `/weights` to get the `best.pt` file
  2. **Boost Model With TensorRT**
      - Go to `YOLOv8-TensorRT-CPP/scripts`, run `python3 pytorch2onnx.py --pt_path <path to your best.pt file>` to get `best.onnx`
      - Open terminal, run `./benchmark --model your/path/to/best.onnx --input your/path/to/frameXXX.jpg --class-names void dirt grass tree pole water sky vehicle object asphalt building log person fence bush concrete barrier uphill downhill puddle mud rubble`
      - Run `./detect_object_image --model your/path/to/best.onnx --input your/path/to/frameXXX.jpg --class-names void dirt grass tree pole water sky vehicle object asphalt building log person fence bush concrete barrier uphill downhill puddle mud rubble` to check the result
      - For analyze all images in a specific folder, copy `runfile.sh` to `YOLOv8-TensorRT-CPP/build`.
        - `chmod +x runfile.sh`
        - `./runfile.sh`
        - **REMEMBER TO CHANGE THE PATH IN `runfile.sh` TO YOUR OWN PATH**

Result will be similar to demo.