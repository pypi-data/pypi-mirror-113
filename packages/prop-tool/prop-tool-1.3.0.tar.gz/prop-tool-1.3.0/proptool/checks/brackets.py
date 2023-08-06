"""
# prop-tool
# Java *.properties file sync checker and syncing tool.
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/prop-tool/
#
"""

from typing import List

from .base.check import Check
from proptool.prop.items import Comment, Translation
from proptool.decorators.overrides import overrides
from proptool.report.group import ReportGroup


# #################################################################################################

class Bracket(object):
    def __init__(self, pos: int, bracket: str):
        self.pos = pos
        self.bracket = bracket


# noinspection PyUnresolvedReferences
class Brackets(Check):
    """
    Checks if brackets are used in translation and if so, ensures proper nesting and checks if all
    opened brackets are closed.
    """

    report_title = 'Brackets'

    # Keep matching elements at the same positions (and in order preserving container!)
    opening: List[str] = ['(', '[', '<', '{']
    closing: List[str] = [')', ']', '>', '}']

    @overrides(Check)
    # Do NOT "fix" the PropFile reference and do not import it, or you step on circular dependency!
    def check(self, translation: 'PropFile', reference: 'PropFile' = None) -> ReportGroup:
        report = ReportGroup(self.report_title)

        for idx, item in enumerate(translation.items):
            # Do not try to be clever and filter() data first, because line_number values will no longer be correct.
            if not isinstance(item, (Translation, Comment)):
                continue

            stack: List[Bracket] = []
            has_errors = False
            for char_idx, current_char in enumerate(item.value):
                position: str = f'{idx + 1}:{char_idx + 1}'

                if current_char in self.opening:
                    # Every opening brace is pushed to the stack.
                    stack.append(Bracket(char_idx, current_char))
                    continue

                if current_char in self.closing:
                    # Every closing brace should take its own pair off the stack

                    if not stack:
                        # If stack is empty, then we had more closing brackets than opening ones.
                        report.create(position, f'No opening character matching "{current_char}".', item.key)
                        # Just show single error per line to avoid flooding.
                        has_errors = True
                        break

                    # Check if what we are about to pop from the stack and see if our current_char matches.
                    expected = self.closing[self.opening.index(stack[-1].bracket)]
                    if current_char == expected:
                        stack.pop()
                        continue

                    # This is not the bracket we were looking for...
                    report.create(position, f'Expected "{expected}", found "{current_char}".', item.key)
                    # Just show single error per line to avoid flooding.
                    has_errors = True
                    break

            if not has_errors and stack:
                # Just show single error per line to avoid flooding.
                bracket = stack[0]
                position: str = f'{idx + 1}:{bracket.pos + 1}'
                report.create(position, f'No closing character for "{bracket.bracket}" found.', item.key)

        return report
