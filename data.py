first_monologue = """\
As I step into UA, I'm greeted by a bustling entrance hall teeming with students. I must admit: With all of my bags and without the official school uniform I feel a bit out of place. A few students look a bit confused, some are whispering and pointing at me. Understandable, I don’t really look like a student here and during the last semester following a villain attack on one of the hero classes the school was rumored to invest a lot into their security system. On the one side that’s amazing, because the hero classes got to move into dorm rooms on the school ground. Free housing! How amazing is that?! In the boarding school I attended the last 6 months I had to pay several hundred Dollars. On the other hand … Well I feel even more out of place than I would anyway. 
As I fumble through my bags, searching for the acceptance letter I received from UA, I can't help but reflect on how I ended up joining this prestigious school in the second semester. During the first semester, I was dealing with some personal challenges that prevented me from applying on time. It was a difficult period, and I felt unsure about my future as a hero. However, fate seemed to have other plans for me.
One day, as I was visiting a local hero agency in my hometown, I happened to cross paths with a UA hero who was on a mission in the area. They noticed my potential and saw something in me that I couldn't see in myself at that time. After a brief conversation, they learned about my situation and offered to recommend me for a late acceptance to UA.
The hero's recommendation carried considerable weight, and the UA administration, understanding the circumstances and recognizing my potential, decided to make an exception and offer me a spot in the second semester. It was a rare and fortunate opportunity, and I couldn't be more grateful for the hero's intervention that changed the course of my life.
“[Player's Name],
We are pleased to inform you that you have been accepted to attend the prestigious U.A. High School, starting from the second semester. Your unique qualities and potential as a hero have not gone unnoticed, and we believe you have the talent to become an outstanding hero in the future.
Enclosed with this letter, you will find all the necessary details for your enrollment at U.A. High School. Please take the time to review the information carefully, as it contains important instructions for your smooth transition into our educational program.
As a late addition, we understand that you might be joining an established class. However, we have full confidence that you will integrate well with your fellow students and thrive in our nurturing environment.
Your journey at U.A. High School will be filled with challenges, growth, and opportunities to showcase your unique abilities. We aim to provide you with the best education and support to help you reach your full potential as a hero.
Upon your arrival, please report to the school's main entrance, where our faculty and staff will be eagerly awaiting your arrival. Feel free to reach out to the school administration if you have any questions or require any assistance before your first day.
Congratulations once again on your acceptance to U.A. High School. We look forward to welcoming you into our heroic community and witnessing the great impact you will undoubtedly make.
Sincerely,
Principal Nezu
U.A. High School”.
As I look around, I spot a green haired boy approaching me. He seems friendly enough, flashing a warm smile my way.\
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
                "type": "dialogue",
                "data": {
                    "line": {
                        "text": "Hey, you must be the new student. I'm Izuku Midoriya, nice to meet you!",
                        "answers": [
                            {
                                "text": "Hi it's me mario",
                                "line": {
                                    "text": "Beach?",
                                    "answers": [
                                        {
                                            "text": "Yes",
                                            "line": None
                                        },
                                        {
                                            "text": "No",
                                            "line": None
                                        }
                                    ]
                                }
                            },
                            {
                                "text": "Hi it's me luigi",
                                "line": None
                            }
                        ]
                    },
                    "character": "katsuki_casual"
                }
            },
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
