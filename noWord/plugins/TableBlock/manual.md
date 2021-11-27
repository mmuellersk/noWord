


### <a name="manual"></a> Table block

Inserts a table.

| Key       |      Description      | Default |
|:----------|:--------------------- | :----- |
| type      |  table                |  
| header    |  list of column headers                |
| keys      |  list of column keys (optional, if not specified header labels are used as keys for the row dictionary)                |
| displayHeader    |  (optional) display header row               | True |
| widths    |  list of column widths              |
| rows    |  list dictioniaries, one for each row, keys are either specified in keys (default) or header (fallback)              |
| repeatRows    |  (optional) The repeatRows argument specifies the number of leading rows that should be repeated when the Table is asked to split itself               | 0 |
| border    |  (optional) border of table       | 0.5 |
| halign    |  (optional) horizontal alignment of table     | CENTER |
| bgcolor    |  (optional) background color of table     |  |
| bordercolor    |  (optional) border color of table     | black |
| style    |  (optional) style name of style from stylesheet used for table     | BodyText |



Example:
```YAML
- type: table
  header: [Key, Value]
  keys: [key, value]
  displayHeader: false
  widths: [4, 12]
  rows:

    - key: <b>Date</b>
      value: '{{res:meta/date}}'
```

Back to [Documentation](../../../README.md#block_basic)
