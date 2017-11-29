## <a name="top"></a> Build-in block types

* [Chapter block](#chapter)
* [Text block](#text)
* [Newpage block](#newpage)
* [List block](#list)
* [Table block](#table)
* [Image block](#image)

### <a name="chapter"></a> Chapter block

| Key       |      Description      |
|:----------|:--------------------- |
| type      |  chapter              |
| title     |  Title of the chapter |
| level     |  chapter hierarchy level (0,1,2,3,...) |
| content   |  First paragraph      |

Example:
```YAML
- type    : chapter
  level   : 0
  title   : Some Chapter Title
  content : >
    Some text...
```

Back to [top](#top)

## <a name="text"></a> Text block

| Key       |      Description      |
|:----------|:--------------------- |
| type      |  text                 |
| content   |  Paragraph            |

Example:
```YAML
- type    : text
  content : >
    Some text...
```

Back to [top](#top)

## <a name="newpage"></a> Newpage block

| Key       |      Description      |
|:----------|:--------------------- |
| type      |  newpage              |

Example:
```YAML
- type    : newpage
```

Back to [top](#top)

## <a name="list"></a> List block

| Key       |      Description      |
|:----------|:--------------------- |
| type      |  list                 |  
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

## <a name="table"></a> Table block

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

## <a name="image"></a> Image block

| Key       |      Description      |
|:----------|:--------------------- |
| type      |  image                 |  
| filename  |  relative filepath to image file        |
| width  |  width of image in cm        |

Example:
```YAML
- type     : image
  width    : 5.6
  filename : /img/test.png
```

Back to [top](#top)
