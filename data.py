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
U.A. High School”

As I look around, I spot a green haired boy approaching me. He seems friendly enough, flashing a warm smile my way.
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
                }
            },
            {
                "type": "dialogue",
                "data": {
                    "character": "deku_school_uniform",
                    "line": {
                        "text": "Hey there! Are you the new transfer student, by any chance?",
                        "answers": [
                            {
                                "preview": "Yes, I am!",
                                "text": "Yes, I am! I just arrived here!",
                                "line": {
                                    "text": "I thought so, nice to meet you!",
                                    "answers": [
                                        {
                                            "preview": "Who are you?",
                                            "text": "Who are you? Shouldn't a teacher be showing me around?",
                                            "line": {
                                                "text": "Oh, I apologize if I gave off the wrong impression. I'm actually a student here, just like you. My name is Midoriya Izuku. I was asked to help you settle in. UA has a student support system, you see!",
                                                "monologue": "So, this guy is a student? He seems nice enough, but I was expecting a teacher. Then again, at such a renowned school the teachers must be really busy all the time … I guess I'll have to make the best of it"
                                            }
                                        },
                                        {
                                            "preview": "Nice to meet you.",
                                            "text": "Nice to meet you. I'm the new transfer student. My name is [player's name].",
                                            "line": {
                                                "text": "Pleasure to meet you, [player's name]! I'm Midoriya Izuku, and I'll be your guide around UA. I'm here to help you settle in and answer any questions you may have.",
                                                "monologue": "He seems friendly enough, even if I was expecting a teacher. I'll try to make the most of this situation."

                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    },

                }
            },
            {
                "type": "dialogue",
                "data": {
                    "character": "deku_school_uniform",
                    "line": {
                        "text": "So, are you ready to start exploring the school?",
                        "answers": [
                            {
                                "preview": "Sure, lead the way!",
                                "text": "Sure, lead the way, Midoriya!",
                                "line": {
                                    "text": "Great! Let's start with the main building. There's so much to see and learn here at UA. Follow me!",
                                    "monologue": "Well, it seems like Midoriya knows his way around. I'll follow him for now and see what UA has to offer."
                                }
                            },
                            {
                                "preview": "I can find my own way around.",
                                "text": "Thanks for the offer, but I think I can find my way around.",
                                "line": {
                                    "text": "Oh, I understand. But I thought I could show you some of the highlights and help you get settled. Just let me know if you change your mind, okay?",
                                    "monologue": "I can be independent and find my own way, plus I’m not happy being shown around by a student instead of a teacher … Though having someone – anyone show me around might not be the worst idea."
                                }

                            }
                        ]
                    }
                }
            }

        ],
    },

    "lockers": {
        "background": "1/entrance01.jpg",
        "escape_points": [
            {
                "position": (500, 500),
                "destination": "hallway"
            }],
        "events": [
            {
                "type": "dialogue",
                "data":
                    {
                        "character": "deku_school_uniform",
                        "line": {
                            "text": "Here we are, the lockers area. It's where students store their belongings during the day. Feel free to choose an empty locker for yourself.",
                            "answers": [
                                {
                                    "preview": "Can you tell me which ones aren’t taken yet?",
                                    "text": "Can you tell me which ones aren’t taken yet, Midoriya?",
                                    "line": {
                                        "text": "Quite a few of them, actually, but it's usually better to choose a locker closer to your classes. That way, you won't have to rush around between breaks. Let's see if there are any available near your first-period classroom.",
                                        "monologue": "Midoriya and I look around the lockers and find one available. Number “095” I should remember that. I’ll take the key for now and sort my belongings in on my first school day."
                                    }
                                }
                            ]
                        }
                    }

            }
        ]
    },

    "hallway": {
        "background": "1/hallway00.jpg",
        "escape_points": [
            {
                "position": (500, 500),
                "destination": "study_hall"
            }
        ],
        "events": [
            {
                "type": "dialogue",
                "data": {
                    "character": "deku_school_uniform",
                    "line": {
                        "text": "This is the main hallway. It's where students gather between classes and during breaks. It's also where you'll find the cafeteria, the library, and the school's main office.",
                        "answers": [
                            {
                                "preview": "I'll make sure to remember that.",
                                "text": " Thanks, I’ll make sure to remember that!",
                                "line": {
                                    "text": " If you have any other questions, feel free to ask.",
                                }
                            },
                            {
                                "preview": "Do students hang out in the hallways?",
                                "text": "Do students often hang out in the hallways, Midoriya?",
                                "line": {
                                    "text": "The hallways can get quite crowded during breaks, and students chat and catch up with friends. However, it's usually better to find a more comfortable spot, like the stairs with couches or the study hall, if you want to relax or study."
                                }
                            }
                        ]
                    }
                }
            }
        ],
    },

    "study_hall": {
        "background": "1/study00.jpg",
        "escape_points": [],
        "events": [],
    },
}
