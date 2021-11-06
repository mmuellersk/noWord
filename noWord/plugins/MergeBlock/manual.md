### <a name="manual"></a> Merge block

Creates a new resource containing all properties from other resources.

The new resource is a deep copy of provided resources.

If the same property is defined in two or more resources, the last one appearing in the resources list will be kept.

| Key       |      Description      | Default |
|:----------|:--------------------- | :------ |
| type      |  list                 |
| alias     | key of the resource<br/> this key is used to access the resource in other blocks     |
| resources | A list of resource aliases to be merged |

Example:
```YAML
- type    : merge
  alias   : redCarConfiguration
  resources : [defaultCarConfiguration, redConfiguration]
```

Back to [Documentation](../../../README.md#block_basic)
