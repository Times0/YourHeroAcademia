scenes_data = {
    "void": {
        "background": "1/void.jpg",
        "escape_points": []
    },
    "entrance": {
        "background": "1/entrance00.jpg",
        "escape_points": [
            {
                "position": (100, 100),
                "destination": "void"
            },
            {
                "position": (200, 200),
                "destination": "lockers"
            }]
    },

    "lockers": {
        "background": "1/entrance01.jpg",
        "escape_points": [
            {
                "position": (100, 100),
                "destination": "entrance"
            }]
    },
}
