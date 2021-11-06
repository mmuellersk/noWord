### <a name="manual"></a> Transformation block

Transforms one or up to 3 resources to new resources using the specified transformation algorithm.


| Key       |      Description      | Default |
|:----------|:--------------------- |:-------------- |
| type      | transformation                |        |
| input     | If this parameter is a string one resource is use as input for the transformation function. If this parameter is  list, up to 3 resources will be used for the transformation function. In this case the signature of the transformation function shall match the number of resources.   |        |
| output    |  Name of the produced output resources.     |        |
| transformation    |  Name of the transformation function. A list of default transformations is implemented in the DefaultTransformation.py. Derived projects can add custom transformations.   |
| params    |  A dictionary of parameters for the transformation function. The function shall use these parameters in its implementation.       |  |

Example:
```YAML
- type   : transformation
  input  : consumer_data
  output : consumer_short
  transformation: flattenFirstToken
  params:
    key      : Url
    seperator: '/'

```

Back to [Documentation](../../../README.md#block_data)
