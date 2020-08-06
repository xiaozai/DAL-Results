# DAL-Results
The reults of DAL and related trackers on the PTB, STC, and CDTB becnmarks.

To save the results for the paper **DAL: A Deep Depth-Aware Long-term Tracke**

**Visualzie Code**
To visualize the raw results one the RGB image on all sequences:
```
python visualize_raw_results.py --raw_results_path XXXXX --dataset CDTB --sequences_path XXXXX
```

To run specific trackers on the specific sequences :
```
python visualize_raw_results.py --raw_results_path XXXXX --dataset STC --sequences_path XXXXX --sequence dog_outside bottle_box --tracker DIMP
```

To save the figures:
```
python visualize_raw_results.py --raw_results_path xxxxx --dataset PTB --sequences_path XXXXX --savefig True --save_path XXXXX
```

**Princeton benchmark (PTB)**
  - [DAL](https://arxiv.org/abs/1912.00660)
  - [ATOM](https://arxiv.org/abs/1811.07628)
  - [DiMP](https://github.com/visionml/pytracking)
  - [OTR](https://github.com/ugurkart/OTR)
  - other variants of DiMP, e.g. DiMP-dseg

**CDTB dataset**
  - dimp50_votd_default_noonline (DAL)
  - dimp50_votd_vot_noonline (DAL)
  - DIMP
  - OTRdataset
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

**STC rgbd benchmark**
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
