# DAL-Results
The reults of DAL and related trackers

To save the results for the paper **DAL: A Deep Depth-Aware Long-term Tracke**

**Visualzie Code**
To visualize the raw results one the RGB image:

```
python visualize_raw_results.py --raw_results_path XXXXX --sequences_path XXXXX
python visualize_raw_results.py --raw_results_path XXXXX --sequences_path XXXXX --sequence dog_outside bottle_box --tracker DIMP
```

**Princeton benchmark (PTB)**
  - [DAL](https://arxiv.org/abs/1912.00660)
  - [ATOM](https://arxiv.org/abs/1811.07628)
  - [DiMP](https://github.com/visionml/pytracking)
  - [OTR](https://github.com/ugurkart/OTR)
  - other variants of DiMP

**CDTB dataset**
  - dimp50_votd_default_noonline (DAL)
  - dimp50_votd_vot_noonline (DAL)
  - DIMP
  - OTR
  - SiamDW_D
  - SiamDW_D_blend
  - SiamFC
  - BACF
  - blend2track_vot
  - CADMS
  - CSRDCF
  - CSR-depth
  - ECO
  - ECOhc
  - ECO-hc-D
  - FuCoLoT
  - KCF
  - KCF-D
  - MDNet
  - MBMD
  - NCC
  - TLD

**OTB dataset**
  - GT
  - DAL
  - our (DAL)
  - DiMP
  - OTR
  - OTR_MVC
  - dimp50_stc_rgbd
  - dimp50_stc_rgbd(0.63)
  - CADMS
  - CSR-DCF
  - CSR_FCLT
  - DSKCF1
  - DSKCF2
  - ECO
  - OAPF
  - PT
  - STC
  - TR_DCF
  - TR_DCF_ICP
  - TR_DCG_ICP_MV
  - TR_DCF_ICP_MV_smart

**PTB***
  - DiMP-rgbd-blend2 (DAL)
  - ATOM
  - DiMP-dseg
  - DiMP
  - OTR

**VOT????**
  - DSKCF1
  - DSKCF2
  - GT
  - OAPF
  - PT
  - STC
