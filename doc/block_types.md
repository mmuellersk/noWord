## <a name="top"></a> Build-in block types

* [Chapter block](#chapter)
* [Text block](#text)

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
| type      |  text              |
| content   |  Paragraph      |

Example:
```YAML
- type    : text
  content : >
    Some text...
```

Back to [top](#top)
