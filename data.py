first_monologue = """As I step into UA, I'm greeted by a bustling entrance hall teeming with students. I must admit: \
With all of my bags and without the official school uniform I feel a bit out of place. A few students look a bit \
confused, some are whispering and pointing at me. Understandable, I don’t really look like a student here and during \
the last semester following a villain attack on one of the hero classes the school was rumored to invest a lot into \
their security system. On the one side that’s amazing, because the hero classes got to move into dorm rooms on the \
school ground. Free housing! How amazing is that?! In the boarding school I attended the last 6 months I had to pay \
several hundred Dollars. On the other hand … Well I feel even more out of place than I would anyway. As I fumble \
through my bags, searching for the acceptance letter I received from UA, I can't help but reflect on how I ended up \
joining this prestigious school in the second semester. During the first semester, I was dealing with some personal \
challenges that prevented me from applying on time. It was a difficult period, and I felt unsure about my future as a \
hero. However, fate seemed to have other plans for me. One day, as I was visiting a local hero agency in my hometown, \
I happened to cross paths with a UA hero who \
was on a mission in the area. They noticed my potential and saw something in me that I couldn't see in myself at that \
time. After a brief conversation, they learned about my situation and offered to recommend me for a late acceptance to \
UA.The hero's recommendation carried considerable weight, and the UA administration, understanding the circumstances \
and recognizing my potential, decided to make an exception and offer me a spot in the second semester. It was a rare \
and fortunate opportunity, and I couldn't be more grateful for the hero's intervention that changed the course of my life.
"""

scenes_data = {
    "void": {
        "background": "1/void.jpg",
        "escape_points": []
    },

    "entrance": {
        "background": "1/entrance00.jpg",
        "escape_points": [
            {
                "position": (686, 417),
                "destination": "lockers"
            }],
        "events": [
            {
                "type": "monologue",
                "data": {
                    "text": first_monologue,
                    "character": {
                        "name": "enji_casual",
                    }
                }
            },
        ],

    },

    "lockers": {
        "background": "1/entrance01.jpg",
        "escape_points": [
            {
                "position": (100, 100),
                "destination": "entrance"
            }],
    },
}
