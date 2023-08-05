Saphyre is a Open Source Python Package for easy computational photography. With one function call, you can automatically create beautiful edits on regular and low light images.

## Table of Contents
* Install
* Quickstart
* Common use
* More information


### Install Saphyre
```
pip install saphyre
```


### Quickstart

Using Saphyre's Computational Photography is a simple calling the `computational_photography()` function:

```python
import saphyre

saphyre.computational_photography("my-image.jpg", "newly_edited_photo.jpg")

```

### Common use

Saphyre works well on both CPU's and GPU's; However, if images are larger than 1 MB, processing takes longer. To combat this, you an shrink your photo slightly using the `lower_size()` function.

```python
import saphyre
from saphyre import helper

smaller_photo = helper.lower_size("big_image.jpg")

# "big_image" has now been reduced in size
saphyre.computational_photography("big_image", "newly_edited_photo.jpg")

```


### More information
For more information on projects from clevrML, please see https://www.clevrml.com or https://apollo.clevrml.com.
