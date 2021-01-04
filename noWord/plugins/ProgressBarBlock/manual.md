### <a name="manual"></a> ProgressBar block

Allows to render progress bar.


| Key       |      Description      | Default |
|:----------|:--------------------- |:-------------- |
| type      |  progressbar                |  
| width     |  (optional) width of progress bar in cm        | width of current document |
| color      |  color of progress bar                |  blue |
| height      |  height of progress bar                |  0.5 cm |
| thickness      |  thickness of progress bar                |  0.5 pt |
| ratio      |  value of progress bar between 0.0 and 1.0                |  |
| criticality      |  if value (ratio) is higher than criticality, progress bar is rendered red                |  |




Example:
```YAML
- type      : progressbar
  ratio     : '0.5'

```

Back to [Documentation](../../../README.md#block_data)
