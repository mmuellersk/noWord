


### <a name="manual"></a> List block

Inserts ordered or unordered list.

| Key       |      Description      | Default |
|:----------|:--------------------- | :------ |
| type      |  list                 |  
| content   |  list of items, can be other dictionaries        |
| numbered  | (optional) add numbers in front of each item     | False |
| start     | (optional) defines start item     | 1 |
| itemspace | (optional) defines start item     | from stylesheet variable itemsInterSpace |
| style     | (optional) defines style name from stylesheet   | BodyText |

Example:
```YAML
- type    : list
  content :
    - Item 1
    - Item 2
    - Item 3
    - ...
```

Back to [Documentation](../../../doc/block_types.md#top)
