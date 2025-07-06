# Reangle-A-Video: 4D Video Generation as Video-to-Video Translation (ICCV 2025)
This repository is the official implementation of [Reangle-A-Video](https://arxiv.org/abs/2503.09151).<br>

[![Project Website](https://img.shields.io/badge/Project-Website-orange)](https://hyeonho99.github.io/reangle-a-video/)
[![arXiv](https://img.shields.io/badge/arXiv-2312.00845-b31b1b.svg)](https://arxiv.org/abs/2503.09151)


## Abstract
**Reangle-A-Video**: A unified framework for synchronized multi-view video generation from a single monocular video, *without relying on any multi-view generative prior*

<details><summary>Full abstract</summary>


> We introduce Reangle-A-Video, a unified framework for generating synchronized multi-view videos from a single input video. Unlike mainstream approaches that train multi-view video diffusion models on large-scale 4D datasets, our method reframes the multi-view video generation task as video-to-videos translation, leveraging publicly available image and video diffusion priors. In essence, Reangle-A-Video operates in two stages. (1) Multi-View Motion Learning: An image-to-video diffusion transformer is synchronously fine-tuned in a self-supervised manner to distill view-invariant motion from a set of warped videos. (2) Multi-View Consistent Image-to-Images Translation: The first frame of the input video is warped and inpainted into various camera perspectives under an inference-time cross-view consistency guidance using DUSt3R, generating multi-view consistent starting images. Extensive experiments on static view transport and dynamic camera control show that Reangle-A-Video surpasses existing methods, establishing a new solution for multi-view video generation.
</details>


## Gallery

<table class="center">
<tr>
  <td style="text-align:center; width=200;"><b>Input video</b></td>
  <td style="text-align:center; width=200;"><b>Generated video1</b></td>
  <td style="text-align:center; width=200;"><b>Generated video2</b></td>
  <td style="text-align:center; width=200;"><b>Generated video3</b></td>
</tr>

<tr>
    <td style="width:200px;">
      <img src="assets/parrot/input.gif" style="width:200px; " alt="Input video">
    </td>
    <td style="width:200px;">
      <img src="assets/parrot/1.gif" style="width:200px; " alt="Generated video1">
    </td>
    <td style="width:200px;">
      <img src="assets/parrot/2.gif" style="width:200px; " alt="Generated video2">
    </td>
    <td style="width:200px;">
      <img src="assets/parrot/3.gif" style="width:200px; " alt="Generated video3">
    </td>
  </tr>

<tr>
    <td style="width:200px;">
      <img src="assets/labrador/input.gif" style="width:200px; " alt="Input video">
    </td>
    <td style="width:200px;">
      <img src="assets/labrador/1.gif" style="width:200px; " alt="Generated video1">
    </td>
    <td style="width:200px;">
      <img src="assets/labrador/2.gif" style="width:200px; " alt="Generated video2">
    </td>
    <td style="width:200px;">
      <img src="assets/labrador/3.gif" style="width:200px; " alt="Generated video3">
    </td>
  </tr>

<tr>
    <td style="width:200px;">
      <img src="assets/frog/input.gif" style="width:200px; " alt="Input video">
    </td>
    <td style="width:200px;">
      <img src="assets/frog/1.gif" style="width:200px; " alt="Generated video1">
    </td>
    <td style="width:200px;">
      <img src="assets/frog/2.gif" style="width:200px; " alt="Generated video2">
    </td>
    <td style="width:200px;">
      <img src="assets/frog/3.gif" style="width:200px; " alt="Generated video3">
    </td>
  </tr>

<tr>
    <td style="width:200px;">
      <img src="assets/cat-girl/input.gif" style="width:200px; " alt="Input video">
    </td>
    <td style="width:200px;">
      <img src="assets/cat-girl/1.gif" style="width:200px; " alt="Generated video1">
    </td>
    <td style="width:200px;">
      <img src="assets/cat-girl/2.gif" style="width:200px; " alt="Generated video2">
    </td>
    <td style="width:200px;">
      <img src="assets/cat-girl/3.gif" style="width:200px; " alt="Generated video3">
    </td>
  </tr>
  
</table>

## Setup
### Install Conda Environment
```
git clone https://github.com/HyeonHo99/Reangle-Video
cd Reangle-Video
conda create -n reangle-video python=3.10
conda activate reangle-video
pip install -r requirements.txt
```

### Install Depth-Anything-V2
```
git clone https://github.com/DepthAnything/Depth-Anything-V2.git extern/Depth-Anything-V2
mkdir -p extern/Depth-Anything-V2/checkpoints && wget -P extern/Depth-Anything-V2/checkpoints https://huggingface.co/depth-anything/Depth-Anything-V2-Large/resolve/main/depth_anything_v2_vitl.pth?download=true -O extern/Depth-Anything-V2/checkpoints/depth_anything_v2_vitl.pth
mv -f assets/temp/run.py extern/Depth-Anything-V2/run.py && mv -f assets/temp/dpt.py extern/Depth-Anything-V2/depth_anything_v2/dpt.py
```



## Codes will be released soon!
- [ ] Release code for Dynamic camera control
- [ ] Release code for Static view transport
