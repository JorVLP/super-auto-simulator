from unittest import TestCase
from unittest.mock import Mock

from sapai.effect.targets import (
    BattlefieldTargetGenerator,
    FirstSelector,
    RandomSelector,
    FriendlyFilter,
)
from sapai.pets import Pet
from sapai.effect.events import Event, EventType


class BattlefieldTargetGeneratorTestCase(TestCase):
    def setUp(self) -> None:
        self.friendly_team = [Mock(Pet) for i in range(5)]
        self.enemy_team = [Mock(Pet) for i in range(5)]
        self.battlefield = self.friendly_team[::-1] + self.enemy_team
        self.event = Event(
            EventType.NONE,
            self.friendly_team[0],
            teams=[self.friendly_team, self.enemy_team],
        )
        self.event_r = Event(
            EventType.NONE,
            self.friendly_team[0],
            teams=[self.friendly_team, self.enemy_team],
        )

    def test_selector(self):
        target = BattlefieldTargetGenerator(
            owner=self.friendly_team[0], selector=FirstSelector()
        )
        self.assertEqual(self.battlefield, target.get(self.event, 10, 0))
        self.assertEqual(self.battlefield, target.get(self.event, 99, 0))

        self.assertEqual(self.battlefield, target.get(self.event_r, 10, 0))
        self.assertEqual(self.battlefield[:5], target.get(self.event_r, 5, 0))
        self.assertEqual([], target.get(self.event_r, 0, 0))

    def test_filter(self):
        target = BattlefieldTargetGenerator(
            owner=self.friendly_team[0],
            selector=FirstSelector(),
            filter_=FriendlyFilter(self.friendly_team[0]),
        )

        self.assertEqual(self.friendly_team[::-1], target.get(self.event, 10, 0))

    def test_random_filter_select(self):
        target = BattlefieldTargetGenerator(
            owner=self.friendly_team[0],
            selector=RandomSelector(),
            filter_=FriendlyFilter(self.friendly_team[0]),
        )

        self.assertEqual(self.friendly_team[::-1], target.get(self.event, 10, 0))
        self.assertEqual(self.friendly_team[::-1], target.get(self.event, 10, 0.99))

        self.assertEqual(self.friendly_team[::-1][:2], target.get(self.event, 2, 0))
        self.assertEqual(self.friendly_team[::-1][-2:], target.get(self.event, 2, 0.99))