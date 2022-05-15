#!/bin/python3

import argparse
import sys
import pgmagick
import pgmagick.api 
import copy 

from dataclasses import dataclass

OUTPUT_DEST='output'

@dataclass
class Vector:
    x: int = 0
    y: int = 0


@dataclass
class OutputData:
    pos: Vector = Vector(0,0)
    size: Vector = Vector(None,None)
    file: str = None



class OutputAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super().__init__(option_strings, dest, nargs, **kwargs)

    def __call__(self, parser, namespace, values=None, option_string=None):
        items_list = getattr(namespace, self.dest, None)
        if not isinstance(items_list, list):
            items_list = list()
        else:
            items_list =  copy.deepcopy(items_list)
        items_list.append(OutputData())
        setattr(namespace, self.dest, items_list)

class OutputSubAction(argparse.Action):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __call__(self, parser, namespace, values=None, option_string=None):
        items_list = getattr(namespace, OUTPUT_DEST, None)
        if not isinstance(items_list, list) or not len(items_list):
            raise ValueError('Not foud prev --output/-o argument') 
        items_list =  copy.deepcopy(items_list)
        item = items_list[-1]
        assert isinstance(item, OutputData)
        if self.dest == 'x':
            item.pos.x = values[0]
        if self.dest == 'y':
            item.pos.y = values[0]
        if self.dest == 'pos':
            item.pos.x = values[0]
            item.pos.y = values[1]
        if self.dest == 'w':
            item.size.x = values[0]
        if self.dest == 'h':
            item.size.y = values[0]
        if self.dest == 's':
            item.size.x = values[0]
            item.size.y = values[1]
        if self.dest == 'f':
            item.file = values[0]

        items_list[-1] = item
        setattr(namespace, OUTPUT_DEST, items_list)

def ParseArguments():
    parser=argparse.ArgumentParser(description="Application is cutting wallpaper on many monitor configurarion", add_help=True)
    parser.add_argument('--input',"-i", dest="input", type=argparse.FileType('r'), help='Image file', nargs=1)
    parser.add_argument('--output',"-o", dest=OUTPUT_DEST, nargs=0 ,help='Output file', action=OutputAction)
    group = parser.add_argument_group('output')
    group.add_argument('--px', nargs=1, dest='x', type=int, help='foo help', action=OutputSubAction)
    group.add_argument('--py', nargs=1, dest='y', type=int, help='foo help', action=OutputSubAction)
    group.add_argument('--pos','-p', nargs=2, dest='pos', type=int, help='foo help', action=OutputSubAction)
    group.add_argument('--sw', nargs=1, dest='w', type=int, help='foo help', action=OutputSubAction)
    group.add_argument('--sh', nargs=1, dest='h', type=int, help='foo help', action=OutputSubAction)
    group.add_argument('--size','-s', nargs=2, dest='s', type=int, help='foo help', action=OutputSubAction)
    group.add_argument('--file','-f', nargs=1, dest='f', type=str, help='foo help', action=OutputSubAction)
    group.add_argument('--verbose', dest='verbose', help='verbose output', action='store_true')
    return parser.parse_args()


def Main():
    args = ParseArguments()
    input_image = pgmagick.api.Image(args.input[0].name, 'r')
    if args.verbose:
        print("Input image \""+args.input[0].name+"\" was open.")
        print("image size: "+str(input_image.width)+"x"+str(input_image.height))

    for output_item in getattr(args, OUTPUT_DEST):
        if output_item.size.x is None:
            output_item.size.x = input_image.width
        if output_item.size.y is None:
            output_item.size.y = input_image.height
        print(output_item)
        print(output_item.size.x)
        print(output_item.size.y)

        new_image_size = pgmagick.Geometry()
        new_image_size.width(int(output_item.size.x))
        new_image_size.height(int(output_item.size.y))
        new_image_size.xOff(int(output_item.pos.x))
        new_image_size.yOff(int(output_item.pos.y))
        new_image = pgmagick.Image(input_image.img)
        new_image.crop(new_image_size);

        new_image.write(output_item.file)

        help(new_image)

        if args.verbose:
            print("Output image \""+output_item.file+"\" was write.")
            print("image size: "+str(new_image.geometry.width())+"x"+str(new_image.geometry.height))

Main()
