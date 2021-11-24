#!/usr/bin/env python
import os
import sys
import glob
sys.path.insert(0, '...')


from noWord.common.PluginInterface import PluginInterface


class TransformationBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'transformation'

    def init(self, context):
        pass

    def prepare(self, block, context):
        pass

    def process(self, block, context):
        input = block["input"]
        outputName = block['output']

        transfo = block['transformation']

        if isinstance(transfo,str):
            params = block['params']

            if transfo in context.doc.availableTransformations :
                outputRes = context.doc.availableTransformations[transfo](input, params, context)
                context.addResource( outputName, outputRes)

        elif isinstance(transfo,list):
            current_params = block['params'][0]
            current_transfo = block['transformation'][0]
            current_outputname = outputName+'_0'

            if current_transfo in context.doc.availableTransformations :
                outputRes = context.doc.availableTransformations[current_transfo](input, current_params, context)
                context.addResource( current_outputname, outputRes)

                for index in range(1,len(transfo)):
                    current_params = block['params'][index]
                    current_transfo = block['transformation'][index]
                    if current_transfo in context.doc.availableTransformations :
                        outputRes = context.doc.availableTransformations[current_transfo](current_outputname, current_params, context)
                        current_outputname = outputName+'_'+str(index)
                        context.addResource( current_outputname, outputRes)


                context.addResource( outputName, outputRes)

        # return empty list
        return []
