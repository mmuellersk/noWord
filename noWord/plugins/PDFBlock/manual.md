
### <a name="manual"></a> PDF block

Inserts content of pdf document.

| Key       |      Description      | Default |
|:----------|:--------------------- | :----- |
| type      |  pdf                 |  
| filename  |  relative filepath to pdf file        |
| width  |  (optional) width of image in cm        | width of current document |
| range  |  (optional) defines range of pages in pdf document to be rendered     | all |
| border  |  (optional) border around pdf document    | 0 |
| xoffset  |  (optional) xoffset in cm to move pdf document    | 0 |
| yoffset  |  (optional) yoffset in cm to move pdf document    | 0 |


Example:
```YAML
- type     : pdf
  width    : 5.6
  filename : /docs/test.pdf
```

Back to [Documentation](../../../doc/block_types.md#external)
