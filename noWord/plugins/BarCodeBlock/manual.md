

### <a name="manual"></a> BarCode block

Inserts different types of barcodes.

| Key       |      Description      | Default    |
|:----------|:--------------------- |:-----------|
| type      |  barcode              |
| value     |  payload of barcode   |  |
| format     |  qr, codacode, code128, code39 | code128 |
| barWidth       |  (optional) width depending on format | 0.15 |
| barHeight  |  (optional) height depending on format | 20 |
| border     |  (optional) border depending on format | 4 |
| quiet     |  (optional) quiet zone depending on format | False |

Example:
```YAML

- type    : barcode
  format  : qr
  version : 1
  barWidth: 32
  barHeight: 32
  border: 2
  value   : 'www.spiegel.de'

- type    : barcode
  format  : code128
  barWidth: 0.3
  barHeight: 8
  value   : 'Z1LPRO25100002340201'
```

Back to [Documentation](../../../README.md#block_basic)
