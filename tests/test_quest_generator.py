"""
Unit tests for TouchGrass Quest Synthesizer.
Verifies all biomes, durations, and output formats.
"""

import unittest
from quest_generator import generate_quest, BIOME_QUEST_TEMPLATES


class TestQuestGenerator(unittest.TestCase):

    def test_all_biomes(self):
        """Verifies quest generation for all supported biomes."""
        biomes = ['park', 'backyard', 'urban', 'trail', 'waterfront']
        for b in biomes:
            quest = generate_quest(duration_mins=15, biome=b)
            self.assertEqual(quest['biome'], b)
            self.assertIn('title', quest)
            self.assertIn('mission_brief', quest)
            self.assertIn('sensory_tasks', quest)
            self.assertEqual(len(quest['sensory_tasks']), 2)
            self.assertIn('verification_challenge', quest)
            self.assertIn('screen_off_cue', quest)

    def test_duration_scaling(self):
        """Verifies duration targets and step estimations scale appropriately."""
        q5 = generate_quest(duration_mins=5, biome='park')
        self.assertEqual(q5['target_duration_mins'], 5)
        self.assertEqual(q5['target_steps'], 300)

        q60 = generate_quest(duration_mins=60, biome='trail')
        self.assertEqual(q60['target_duration_mins'], 60)
        self.assertEqual(q60['target_steps'], 4500)

    def test_unknown_biome_fallback(self):
        """Verifies graceful fallback to park for unknown biome strings."""
        quest = generate_quest(duration_mins=20, biome='space_station')
        self.assertEqual(quest['biome'], 'park')


if __name__ == '__main__':
    unittest.main()
