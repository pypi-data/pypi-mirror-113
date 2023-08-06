# pyxelstitch
> Simple, matplotlib based tool for hand-labeling the two-image correspondences


## Install

`pip install pixelstitch`

## How to use

Let's test our annotator on a sample project. It needs a list of triplets: (`path_to_img1`, `path_to_img2`, `path_to_corrs_to_save`).

```python
import os
rootdir = 'sample_project'
pairs = os.listdir(rootdir)
img_pairs_list = []
for p in pairs:
    if p == '.DS_Store':
        continue
    cur_dir = os.path.join(rootdir, p)
    img_pairs_list.append((os.path.join(cur_dir, '01.png'),
                           os.path.join(cur_dir, '02.png'),
                           os.path.join(cur_dir, 'corrs.txt')))

print (img_pairs_list)
```

    [('sample_project/ministry/01.png', 'sample_project/ministry/02.png', 'sample_project/ministry/corrs.txt'), ('sample_project/petrzin/01.png', 'sample_project/petrzin/02.png', 'sample_project/petrzin/corrs.txt')]


    /opt/homebrew/Caskroom/miniforge/base/envs/python39/lib/python3.9/site-packages/ipykernel/ipkernel.py:283: DeprecationWarning: `should_run_async` will not call `transform_cell` automatically in the future. Please pass the result to `transformed_cell` argument and any exception that happen during thetransform in `preprocessing_exc_tuple` in IPython 7.17 and above.
      and should_run_async(code)


Now we are ready to initialize `CorrespondenceAnnotator`. Don't forget to declare magic command ```%matplotlib notebook```.
**WITHOUT MAGIC IT WOULD NOT WORK**

You also should explicitly specify, if you want to save (and possibly over-write previous better annotation) current correspondences automatically when clicking on **prev** and **next** buttons for going to the next pair. 

```python
%matplotlib notebook
from pixelstitch.core import *
CA = CorrespondenceAnnotator(img_pairs_list, save_on_next=True)
```

    /opt/homebrew/Caskroom/miniforge/base/envs/python39/lib/python3.9/site-packages/ipykernel/ipkernel.py:283: DeprecationWarning: `should_run_async` will not call `transform_cell` automatically in the future. Please pass the result to `transformed_cell` argument and any exception that happen during thetransform in `preprocessing_exc_tuple` in IPython 7.17 and above.
      and should_run_async(code)


Now we can run the annotation. 

**Left-click** on the image to add a point 

**right-click** -- to remove the point from both images. 

### Matplotlib shortcuts:

- **o** for zoom 
- **p** for pan (move)

It is also recommended to set full page width for the jupyter


```python
from IPython.core.display import display, HTML
display(HTML("<style>.container { width:95% !important; }</style>"))
CA.start(figsize=(12,7))
```
