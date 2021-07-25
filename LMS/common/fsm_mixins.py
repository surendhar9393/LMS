from __future__ import unicode_literals

from collections import defaultdict
from fsm_admin.mixins import FSMTransitionMixin as FSMTransitionMixin_


class FSMTransitionMixin(FSMTransitionMixin_):
    """
    Overriding this class as the following method has a bug
    """

    def get_transition_hints(self, obj):
        """
        See `fsm_transition_hints` templatetag.
        """
        hints = defaultdict(list)
        transitions = self._get_possible_transitions(obj)

        # Step through the conditions needed to accomplish the legal state
        # transitions, and alert the user of any missing condition.
        # TODO?: find a cleaner way to enumerate conditions methods?
        for transition in transitions:
            for condition in transition.conditions:

                # If the condition is valid, then we don't need the hint
                if condition(obj):
                    continue

                # if the transition is hidden, we don't need the hint
                # Change by Nikhil
                if not transition.custom.get('admin', self.default_disallow_transition):
                    continue

                hint = getattr(condition, 'hint', '')
                if hint:
                    if hasattr(transition, 'custom') and transition.custom.get(
                            'button_name'):
                        hints[transition.custom['button_name']].append(hint)
                    else:
                        hints[transition.name.title()].append(hint)

        return dict(hints)
