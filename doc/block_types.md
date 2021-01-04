## <a name="top"></a> Build-in block types

* [Chapter block](#chapter)
* [Text block](#text)
* [Newpage block](#newpage)
* [vSpace block](#vspace)
* [List block](#list)
* [Table block](#table)
* [Image block](#image)
* [PDF block](#pdf)
* [Tabel of Content block](#toc)
* [Line block](#line)
* [Resouce block](../noWord/plugins/ResourceBlock/manual.md#manual)

### <a name="chapter"></a> Chapter block

Inserts headings.

| Key       |      Description      |
|:----------|:--------------------- |
| type      |  chapter              |
| title     |  title of the chapter |
| level     |  (optional) chapter hierarchy level (0,1,2,3,...) |

Example:
```YAML
- type    : chapter
  level   : 0
  title   : Some Chapter Title
  content : >
    Some text...
```

Back to [top](#top)

### <a name="text"></a> Text block

Insert standard paragraph.

| Key       |      Description      |
|:----------|:--------------------- |
| type      |  text                 |
| font      |  (optional) font name defined in template                 |
| content   |  Paragraph            |

Example:
```YAML
- type    : text
  content : >
    Some text...
```

Back to [top](#top)

### <a name="newpage"></a> Newpage block

Add newpage to document flow.

| Key       |      Description      |
|:----------|:--------------------- |
| type      |  newpage              |
| orientation      |  (optional) orientation of new page              |

Example:
```YAML
- type    : newpage
```

Back to [top](#top)

### <a name="vspace"></a> vSpace block

Inserts a vertical space in the document flow.

| Key       |      Description      |
|:----------|:--------------------- |
| type      |  vspace                 |  
| height  |  (optional) height of the space in cm        |

Example:
```YAML
- type     : vspace
  height   : 5.6
```

Back to [top](#top)

### <a name="list"></a> List block

Inserts ordered or unordered list.

| Key       |      Description      |
|:----------|:--------------------- |
| type      |  list                 |  
| numbered  | (optional) (true) / false          |
| content   |  list of items, can be other dictionaries        |

Example:
```YAML
- type    : list
  content :
    - Item 1
    - Item 2
    - Item 3
    - ...
```

Back to [top](#top)

### <a name="table"></a> Table block

Inserts a table.

| Key       |      Description      |
|:----------|:--------------------- |
| type      |  table                |  
| header    |  list of column headers                |
| keys      |  list of column keys (optional, if not specified header labels are used as keys for the row dictionary)                |
| displayHeader    |  true / false               |
| widths    |  list of column widths              |
| rows    |  list dictioniaries, one for each row, keys are either specified in keys (default) or header (fallback)              |



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

Back to [top](#top)

### <a name="image"></a> Image block

Inserts an image.

| Key       |      Description      |
|:----------|:--------------------- |
| type      |  image                 |  
| filename  |  relative filepath to image file        |
| caption      |  caption under the image                 |  
| width  |  width of image in cm        |

Example:
```YAML
- type     : image
  width    : 5.6
  filename : /img/test.png
```

Back to [top](#top)

### <a name="pdf"></a> PDF block

Inserts content of pdf document.

| Key       |      Description      |
|:----------|:--------------------- |
| type      |  pdf                 |  
| filename  |  relative filepath to pdf file        |
| width  |  width of image in cm        |

Example:
```YAML
- type     : pdf
  width    : 5.6
  filename : /docs/test.pdf
```

Back to [top](#top)

### <a name="vspace"></a> vSpace block

Inserts a vertical space in the document flow.

| Key       |      Description      |
|:----------|:--------------------- |
| type      |  vspace                 |  
| height  |  (optional) height of the space in cm        |

Example:
```YAML
- type     : vspace
  height   : 5.6
```

Back to [top](#top)

### <a name="toc"></a> Table of content block

Inserts table of content calculated from chapter blocks.

| Key       |      Description      |
|:----------|:--------------------- |
| type      |  toc                 |  

Example:
```YAML
- type     : toc
```

Back to [top](#top)

### <a name="line"></a> Line block

Inserts vertical line.

| Key       |      Description      |
|:----------|:--------------------- |
| type      |  line                 |  
| dashes      |  (optional) (true) / false     |  
| dashes      |  (optional) (true) / false OR list of two integers for custom dash (space, section)   |  
| width      |  (optional) width in cm     |  
| color      |  (optional) color of the line     |  
| thickness      |  (optional) thickness of the line in cm   |  
| rounded      |  (optional) (true) / false     |  

Example:
```YAML
- type     : line
```

Back to [top](#top)
