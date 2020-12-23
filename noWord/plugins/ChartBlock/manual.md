### <a name="manual"></a> Chart block

Allows render charts with loaded data.


| Key       |      Description      | Default |
|:----------|:--------------------- |:-------------- |
| type      |  chart                |   |
| data  |  data used for display of chart, can be resources or list object     |
| plotdata  |  data used for display of chart, can be only resources  (y valus)   |
| xvalues  |  x values    |
| width     |  (optional) width of chart in cm        | width of current document |
| mode     |  (optional) type of chart, possible value are:<br/>- linechart<br/>- barchart<br/>- plotchart<br/>- piechart | linechart |
| labelAngles  |      |
| labelXOffsets  |      |
| labelYOffsets  |      |
| linecolors  |      |
| barColors  |      |
| strokeWidth  |      |
| displayBarLabels  |      |
| lineWidths  |      |
| backgroundColor  |      |
| borderColor  |      |
| lineLabelFormat  |      |
| yAxisMin  |      |
| yAxisMax  |      |
| yAxisStep  |      |


Example:
```YAML
- type        : chart

```

Back to [Documentation](../../../README.md#block_data)
