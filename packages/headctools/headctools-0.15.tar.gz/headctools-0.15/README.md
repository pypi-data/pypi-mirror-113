![headctools](headctools/assets/imgs/logo/bright-bg-stroke.svg)

This tool includes a bunch of algorithms for preprocessing CT images & 
PyTorch based models for performing brain segmentation or skull 
reconstruction on craniectomy images.

The implemented convolutional neural networks are based on the [U-Net](https://arxiv.org/abs/1505.04597) model,
which was adapted to these particular problems.

### Requirements

You should have Python 3.7+ installed in your system. If you are using the 
registrarion commands, you should manually install [FSL](https://fsl.fmrib.ox.ac.uk)

#### Package install 

For installing the package using pip, run the following command:

```sh
pip install headctools
```

You can check some usage examples in the [colab notebook](https://colab.research.google.com/drive/16i30BKtAfA1D9NLVs26ddjs87tmiU6xR?usp=sharing) 
and the [readthedocs page](https://headctools.readthedocs.io/en/latest/).

### Citing our work

If you have found this repo useful, please consider citing our work

```
@incollection{Matzkin2020,
  doi = {10.1007/978-3-030-59713-9_38},
  url = {https://doi.org/10.1007/978-3-030-59713-9_38},
  year = {2020},
  publisher = {Springer International Publishing},
  pages = {390--399},
  author = {Franco Matzkin and Virginia Newcombe and Susan Stevenson and Aneesh Khetani and Tom Newman and Richard Digby and Andrew Stevens and Ben Glocker and Enzo Ferrante},
  title = {Self-supervised Skull Reconstruction in Brain {CT} Images with Decompressive Craniectomy},
  booktitle = {Medical Image Computing and Computer Assisted Intervention {\textendash} {MICCAI} 2020}
}
```

Project logo icons made by Pixel perfect from [www.flaticon.com](www.flaticon.com)