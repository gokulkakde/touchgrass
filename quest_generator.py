"""
Micro-Expedition Quest Synthesizer for TouchGrass AI.
Generates structured, sensory-rich, low-screen outdoor missions grounded in biomes and time constraints.
"""

import uuid
import random

BIOME_QUEST_TEMPLATES = {
    'park': [
        {
            'title': 'Canopy & Vein Recon',
            'sensory_focus': 'Botanical & Texture',
            'mission_brief': 'Head to the nearest patch of public greenery and inspect leaf architecture.',
            'sensory_tasks': [
                'Touch the bark of two different tree species and compare their rough and smooth textures.',
                'Find a shaded spot, sit or stand still for 60 seconds, and notice the breeze on your face.'
            ],
            'verification_challenge': 'Capture one clear photograph of a fallen or living leaf with distinct vein patterns.'
        },
        {
            'title': 'The Avian Soundscape Survey',
            'sensory_focus': 'Acoustic Observation',
            'mission_brief': 'Track bird vocalizations while moving quietly through the park.',
            'sensory_tasks': [
                'Pause near a dense shrub or tree line and isolate 3 distinct wildlife sounds without looking around.',
                'Walk 500 paces without glancing at any digital device.'
            ],
            'verification_challenge': 'Photograph a wild bird, a pollinator on a flower, or a nesting hollow in a tree.'
        },
        {
            'title': 'The Deep Soil Grounding Loop',
            'sensory_focus': 'Tactile & Grounding',
            'mission_brief': 'Break away from concrete walkways and step onto natural grass or earth.',
            'sensory_tasks': [
                'Stand on living grass or soil; take 10 deep belly breaths with your eyes closed.',
                'Inspect the base of a large tree for moss, lichen, or fungi colonies.'
            ],
            'verification_challenge': 'Photograph a patch of moss, lichen, or wild mushroom growing on wood or soil.'
        }
    ],
    'backyard': [
        {
            'title': 'Micro-Ecosystem Micro-Tour',
            'sensory_focus': 'Observation & Detail',
            'mission_brief': 'Explore the miniature biodiversity living right outside your backdoor.',
            'sensory_tasks': [
                'Kneel down and inspect a 1-foot square patch of soil or grass for 2 minutes.',
                'Find a plant in transition (blooming, seeding, or wilting) and examine its stem.'
            ],
            'verification_challenge': 'Photograph a tiny seedling, flowering weed, or garden plant in natural daylight.'
        },
        {
            'title': 'The 10-Minute Sun & Sky Reset',
            'sensory_focus': 'Circadian Re-alignment',
            'mission_brief': 'Step into direct or indirect outdoor light to reset your ocular focus.',
            'sensory_tasks': [
                'Face the open sky (away from direct sun glare) and let your eyes relax on the horizon for 3 minutes.',
                'Feel the ambient outdoor air temperature on your bare hands and forearms.'
            ],
            'verification_challenge': 'Photograph the tree canopy, garden foliage, or outdoor flora against the open sky.'
        }
    ],
    'urban': [
        {
            'title': 'The Urban Foliage Breakthrough',
            'sensory_focus': 'Contrast & Resiliency',
            'mission_brief': 'Discover resilient nature thriving in the middle of concrete and asphalt.',
            'sensory_tasks': [
                'Walk 600 paces away from your building without checking any message or notification.',
                'Spot a resilient dandelion, weed, or fern emerging through sidewalk masonry.'
            ],
            'verification_challenge': 'Photograph resilient flora growing from a crack, street tree basin, or masonry edge.'
        },
        {
            'title': 'The Sidewalk Canopy Trek',
            'sensory_focus': 'Vertical Observation',
            'mission_brief': 'Look up above street level to notice city trees and avian pathways.',
            'sensory_tasks': [
                'Notice the pattern of sunlight filtering through street tree branches onto the pavement.',
                'Listen specifically for wind rustling leaves over city traffic hum.'
            ],
            'verification_challenge': 'Photograph a street tree trunk, flowering boulevard shrub, or city park bench.'
        }
    ],
    'trail': [
        {
            'title': 'Deep Forest Pathfinding',
            'sensory_focus': 'Proprioception & Immersion',
            'mission_brief': 'Immerse in unpaved nature and align your breathing with your stride.',
            'sensory_tasks': [
                'Walk continuously for 12 minutes on unpaved dirt, noticing each heel-to-toe strike.',
                'Find an ancient boulder or fallen timber and touch its sun-warmed surface.'
            ],
            'verification_challenge': 'Photograph wild forest undergrowth, evergreen needles, or a rock formation.'
        },
        {
            'title': 'The Wild Biome Scavenger',
            'sensory_focus': 'Biodiversity Search',
            'mission_brief': 'Spot evidence of active woodland life along the trail margin.',
            'sensory_tasks': [
                'Stop at a trail bend, breathe the scent of damp pines or damp soil for 1 full minute.',
                'Spot animal tracks, seed pods, or pine cones scattered on the forest floor.'
            ],
            'verification_challenge': 'Photograph a pine cone, acorn, wild berry, or natural fungus along the trail.'
        }
    ],
    'waterfront': [
        {
            'title': 'Ripples & Shoreline Focus',
            'sensory_focus': 'Aquatic Acoustics',
            'mission_brief': 'Head toward open water to experience negative ions and water motion.',
            'sensory_tasks': [
                'Watch moving water ripples for 3 uninterrupted minutes to release mental screen strain.',
                'Listen to the acoustic cadence of water meeting shore, rocks, or reeds.'
            ],
            'verification_challenge': 'Photograph shoreline reeds, water lilies, river stones, or aquatic waterfowl.'
        }
    ]
}


def generate_quest(duration_mins=15, biome='park'):
    """
    Synthesizes a structured micro-quest based on duration and biome.
    Returns structured JSON with strict screen-off instructions.
    """
    biome_key = biome.lower() if biome.lower() in BIOME_QUEST_TEMPLATES else 'park'
    templates = BIOME_QUEST_TEMPLATES[biome_key]
    template = random.choice(templates)

    quest_id = f"quest_{uuid.uuid4().hex[:8]}"

    # Adjust pace/distance recommendations based on duration
    if duration_mins <= 5:
        duration_desc = "5-Minute Quick Breath"
        step_target = 300
    elif duration_mins <= 15:
        duration_desc = "15-Minute Micro-Expedition"
        step_target = 1000
    elif duration_mins <= 30:
        duration_desc = "30-Minute Nature Loop"
        step_target = 2200
    else:
        duration_desc = "60-Minute Deep Disconnect Trek"
        step_target = 4500

    return {
        'quest_id': quest_id,
        'title': template['title'],
        'biome': biome_key,
        'biome_display': biome_key.capitalize(),
        'target_duration_mins': duration_mins,
        'duration_display': duration_desc,
        'target_steps': step_target,
        'sensory_focus': template['sensory_focus'],
        'mission_brief': template['mission_brief'],
        'sensory_tasks': template['sensory_tasks'],
        'verification_challenge': template['verification_challenge'],
        'screen_off_cue': 'Your mission is set. Put your device in your pocket, close this screen, and step outside.',
        'safety_tips': [
            'Stay aware of your physical surroundings, terrain, and traffic.',
            'Carry water if walking under direct sun.',
            'Leave no trace: do not pick or disturb wild flora.'
        ]
    }
