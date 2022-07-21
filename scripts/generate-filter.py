#!/usr/bin/env python3
'''A python script to convert a hex color code to a CSS filter.

This is a python port of <https://codepen.io/sosuke/pen/Pjoqqp>.
The original is licensed under the 0BSD license, so this port retains that license.

Zero-Clause BSD

Permission to use, copy, modify, and/or distribute this software for any purpose with or without
fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS
SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
OF THIS SOFTWARE.
'''

import math
import random
import re
import sys
from typing import overload, List, Optional, Union
from typing_extensions import TypedDict

# XXX: Most of this code was uncommented when it was ported, and remains uncommented. There's a lot
# XXX: of math here, and figuring out/documenting how it works is left as an exercise to the reader

HELP_TEXT = '''usage: python generate-filter.py [--help] <hex_color>

<hex_color>: any 3 or 6 digit hexadecimal color code, optionally prefixed with a '#'
    Ex: '#abc' 'a1b2c3'

--help: show this help text and exit
'''


# Num is used to emulate javascript's `Number` type,
# as int and float are used interchangeably in this code
Num = Union[int, float]

HSL = TypedDict('HSL', {'h': Num, 's': Num, 'l': Num})

SolvedResult = TypedDict('SolvedResult', {'values': List[Num], 'loss': Num, 'filter': str})

IntermediateSolvedResult = TypedDict('IntermediateSolvedResult', {
    'values': List[Num],
    'loss': Num,
})


class Color:
    def __init__(self, r: Num, g: Num, b: Num):
        self._r, self._g, self._b = r, g, b

    def __str__(self) -> str:
        return f'rgb({round(self.r)}, {round(self.g)}, {round(self.b)})'

    @property
    def r(self) -> Num:
        return self._r

    @r.setter
    def r(self, value: Num) -> None:
        self._r = self.clamp(value)

    @property
    def g(self) -> Num:
        return self._g

    @g.setter
    def g(self, value: Num) -> None:
        self._g = self.clamp(value)

    @property
    def b(self) -> Num:
        return self._b

    @b.setter
    def b(self, value: Num) -> None:
        self._b = self.clamp(value)

    def hueRotate(self, angle: float = 0) -> None:
        # python's math.pi is equal to JS' Math.PI so we'll get the exact same result as the JS
        angle = angle / 180 * math.pi
        sin = math.sin(angle)
        cos = math.cos(angle)

        self.multiply(
            0.213 + cos * 0.787 - sin * 0.213,
            0.715 - cos * 0.715 - sin * 0.715,
            0.072 - cos * 0.072 + sin * 0.928,
            0.213 - cos * 0.213 + sin * 0.143,
            0.715 + cos * 0.285 + sin * 0.140,
            0.072 - cos * 0.072 - sin * 0.283,
            0.213 - cos * 0.213 - sin * 0.787,
            0.715 - cos * 0.715 + sin * 0.715,
            0.072 + cos * 0.928 + sin * 0.072,
        )

    def grayscale(self, value: int = 1) -> None:
        self.multiply(
            0.2126 + 0.7874 * (1 - value),
            0.7152 - 0.7152 * (1 - value),
            0.0722 - 0.0722 * (1 - value),
            0.2126 - 0.2126 * (1 - value),
            0.7152 + 0.2848 * (1 - value),
            0.0722 - 0.0722 * (1 - value),
            0.2126 - 0.2126 * (1 - value),
            0.7152 - 0.7152 * (1 - value),
            0.0722 + 0.9278 * (1 - value),
        )

    def sepia(self, value: Num = 1) -> None:
        self.multiply(
            0.393 + 0.607 * (1 - value),
            0.769 - 0.769 * (1 - value),
            0.189 - 0.189 * (1 - value),
            0.349 - 0.349 * (1 - value),
            0.686 + 0.314 * (1 - value),
            0.168 - 0.168 * (1 - value),
            0.272 - 0.272 * (1 - value),
            0.534 - 0.534 * (1 - value),
            0.131 + 0.869 * (1 - value),
        )

    def saturate(self, value: Num = 1) -> None:
        self.multiply(
            0.213 + 0.787 * value,
            0.715 - 0.715 * value,
            0.072 - 0.072 * value,
            0.213 - 0.213 * value,
            0.715 + 0.285 * value,
            0.072 - 0.072 * value,
            0.213 - 0.213 * value,
            0.715 - 0.715 * value,
            0.072 + 0.928 * value,
        )

    def multiply(self, *args: float) -> None:
        newR = self.clamp(self.r * args[0] + self.g * args[1] + self.b * args[2])
        newG = self.clamp(self.r * args[3] + self.g * args[4] + self.b * args[5])
        newB = self.clamp(self.r * args[6] + self.g * args[7] + self.b * args[8])
        self.r = newR
        self.g = newG
        self.b = newB

    def brightness(self, value: Num = 1) -> None:
        self.linear(value)

    def contrast(self, value: Num = 1) -> None:
        self.linear(value, -(0.5 * value) + 0.5)

    def linear(self, slope: Num = 1, intercept: Num = 0) -> None:
        self.r = self.clamp(self.r * slope + intercept * 255)
        self.g = self.clamp(self.g * slope + intercept * 255)
        self.b = self.clamp(self.b * slope + intercept * 255)

    def invert(self, value: Num = 1) -> None:
        self.r = self.clamp((value + self.r / 255 * (1 - 2 * value)) * 255)
        self.g = self.clamp((value + self.g / 255 * (1 - 2 * value)) * 255)
        self.b = self.clamp((value + self.b / 255 * (1 - 2 * value)) * 255)

    def hsl(self) -> HSL:
        # Code taken from https://stackoverflow.com/a/9493060/2688027, licensed under CC BY-SA.
        r = self.r / 255
        g = self.g / 255
        b = self.b / 255
        max_ = max(r, g, b)
        min_ = min(r, g, b)
        h = (max_ + min_) / 2
        s, l = h, h  # noqa: E741

        if (max_ == min_):
            h, s = 0, 0
        else:
            d = max_ - min_
            if l > 0.5:
                s = d / (2 - max_ - min_)
            else:
                s = d / (max_ + min_)

            if max_ == r:
                h = (g - b) / d + (6 if g < b else 0)
            elif max_ == g:
                h = (b - r) / d + 2
            elif max_ == b:
                h = (r - g) / d + 4

            h /= 6

        return {
            'h': h * 100,
            's': s * 100,
            'l': l * 100,
        }

    @overload
    def clamp(self, value: int) -> int: ...
    @overload
    def clamp(self, value: float) -> float: ...

    def clamp(self, value: Num) -> Num:
        if (value > 255):
            value = 255
        elif (value < 0):
            value = 0
        return value


class Solver:
    def __init__(self, target: Color):
        self.target = target
        self.targetHSL = target.hsl()
        self.reusedColor = Color(0, 0, 0)

    def solve(self) -> SolvedResult:
        result = self.solveNarrow(self.solveWide())
        return {
            'values': result['values'],
            'loss': result['loss'],
            'filter': self.css(result['values']),
        }

    def solveWide(self) -> IntermediateSolvedResult:
        A = 5
        c = 15
        a = [60, 180, 18000, 600, 1.2, 1.2]

        best: IntermediateSolvedResult = {'values': [], 'loss': math.inf}
        i = 0
        while best['loss'] > 25 and i < 3:
            i += 1
            initial: List[Num] = [50, 20, 3750, 50, 100, 100]
            result = self.spsa(A, a, c, initial, 1000)
            if result['loss'] < best['loss']:
                best = result

        return best

    def solveNarrow(
        self,
        wide: IntermediateSolvedResult
    ) -> IntermediateSolvedResult:
        A: Num = wide['loss']
        c = 2
        A1 = A + 1
        a = [0.25 * A1, 0.25 * A1, A1, 0.25 * A1, 0.2 * A1, 0.2 * A1]
        return self.spsa(A, a, c, wide['values'], 500)

    def spsa(
        self,
        A: Num,
        a: List[Num],
        c: Num,
        values: List[Num],
        iters: int
    ) -> IntermediateSolvedResult:
        alpha = 1
        gamma = 0.16666666666666666

        best = []
        bestLoss = math.inf
        deltas = []
        highArgs = []
        lowArgs = []

        for k in range(iters):
            ck = c / pow(k + 1, gamma)
            for i in range(6):
                deltas.append(random.choice((-1, 1)))
                highArgs.append(values[i] + ck * deltas[i])
                lowArgs.append(values[i] - ck * deltas[i])

            lossDiff = self.loss(highArgs) - self.loss(lowArgs)
            for i in range(6):
                g = lossDiff / (2 * ck) * deltas[i]
                ak = a[i] / pow(A + k + 1, alpha)
                values[i] = self.fix(values[i] - ak * g, i)

            loss = self.loss(values)
            if (loss < bestLoss):
                best = values.copy()
                bestLoss = loss

        return {'values': best, 'loss': bestLoss}

    @classmethod
    def fix(self, value: Num, idx: Num) -> Num:
        max_ = 100
        if idx == 2:  # saturate
            max_ = 7500
        elif idx == 4 or idx == 5:  # brightness or contrast
            max_ = 200

        if idx == 3:  # hue-rotate
            if value > max_:
                value %= max_
            elif value < 0:
                value = max_ + value % max_
        elif value < 0:
            value = 0
        elif value > max_:
            value = max_

        return value

    def loss(self, filters: List[Num]) -> Num:
        # Argument is array of percentages.
        color = self.reusedColor
        color.r, color.g, color.b = 0, 0, 0

        color.invert(filters[0] / 100)
        color.sepia(filters[1] / 100)
        color.saturate(filters[2] / 100)
        color.hueRotate(filters[3] * 3.6)
        color.brightness(filters[4] / 100)
        color.contrast(filters[5] / 100)

        colorHSL = color.hsl()
        return (
          abs(color.r - self.target.r) +
          abs(color.g - self.target.g) +
          abs(color.b - self.target.b) +
          abs(colorHSL['h'] - self.targetHSL['h']) +
          abs(colorHSL['s'] - self.targetHSL['s']) +
          abs(colorHSL['l'] - self.targetHSL['l'])
        )

    def css(self, filters: List[Num]) -> str:
        def fmt(idx: int, multiplier: Num = 1) -> Num:
            return round(filters[idx] * multiplier)

        return f'filter: invert({fmt(0)}%) sepia({fmt(1)}%) saturate({fmt(2)}%) '\
               f'hue-rotate({fmt(3, 3.6)}deg) brightness({fmt(4)}%) contrast({fmt(5)}%);'


def hexToRgb(hex_: str) -> Optional[List[int]]:
    # Expand shorthand form (e.g. "03F") to full form (e.g. "0033FF")
    shorthandRegex = re.compile(r'^#?([a-f\d])([a-f\d])([a-f\d])$', re.IGNORECASE)
    shorthand = shorthandRegex.match(hex_)
    if shorthand:
        r, g, b = shorthand.groups()
        hex_ = f'{r}{r}{g}{g}{b}{b}'

    hex_regex = re.compile(r'^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$', re.IGNORECASE)
    result = hex_regex.match(hex_)
    if not result:
        raise ValueError(f"input {hex_} isn't a valid hex code")
    if result:
        return [
            int(result.groups()[0], 16),
            int(result.groups()[1], 16),
            int(result.groups()[2], 16),
        ]
    else:
        return None


def main(input_target: str, attempts: int = 5) -> None:
    rgb = hexToRgb(input_target)

    if rgb is None:
        exit('not a valid hex color\n\n' + HELP_TEXT)

    color = Color(rgb[0], rgb[1], rgb[2])
    solver = Solver(color)
    result = solver.solve()

    best = result

    for i in range(attempts-1):
        result = solver.solve()
        if result['loss'] < best['loss']:
            best = result

    loss = result['loss']

    if loss < 1:
        lossMsg = 'This is a perfect result.'
    elif loss < 5:
        lossMsg = 'The is close enough.'
    elif loss < 15:
        lossMsg = 'The color is somewhat off. Consider running it again.'
    else:
        lossMsg = 'The color is extremely off. Run it again!'

    print(lossMsg)
    print(best['filter'])


if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] == '--help':
        exit(HELP_TEXT)

    main(sys.argv[1])
