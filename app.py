from pathlib import Path
from flask import Flask, render_template

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
VIDEO_EXTS = {".mp4", ".webm", ".ogg", ".mov", ".m4v"}
AUDIO_EXTS = {".mp3", ".wav", ".ogg", ".m4a"}


def discover_files(folder: Path, exts: set[str]) -> list[str]:
    if not folder.exists():
        return []
    files = []
    for path in sorted(folder.iterdir()):
        if path.is_file() and path.suffix.lower() in exts:
            files.append("/static/" + path.relative_to(STATIC_DIR).as_posix())
    return files


def discover_one(folder: Path, exts: set[str]) -> str | None:
    files = discover_files(folder, exts)
    return files[0] if files else None


def opening_memories(images: list[str]) -> list[dict]:
    fallback = [
        "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1511988617509-a57c8a288659?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1520854221256-17451cc331bf?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1511285560929-80b456fea0bc?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1464349095431-e9a21285b5f3?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=1200&q=80",
    ]

    messages = [
        ("Memory", "A little memory I will always keep ❤️", "Some moments stay quietly in the heart forever."),
        ("Memory", "One of my favorite versions of us ✨", "A version of us I always smile remembering."),
        ("Memory", "A frame full of love and comfort", "This is what peace looks like to me."),
        ("Memory", "Us, and all the warmth that comes with it", "Every moment with you feels safe."),
        ("Memory", "A beautiful moment I never get tired of", "Even today this still feels special."),
        ("Memory", "Proof that ordinary moments with you are special", "Because you make everything meaningful."),
        ("Memory", "Another chapter of my favorite story", "And I would relive it again and again."),
        ("Memory", "A small memory, a big feeling ❤️", "Some memories quietly become priceless."),
        ("Memory", "Still one of my happiest moments", "One of the many reasons I smile."),
        ("Memory", "You and me — my favorite place", "My safest place has always been beside you."),
    ]

    source = images if images else fallback
    result = []
    for index, image in enumerate(source[:10]):
        year, title, description = messages[index % len(messages)]
        result.append({"year": year, "title": title, "description": description, "image": image})
    return result


def timeline_items(images: list[str]) -> list[dict]:
    timeline_images = [
        "/static/images/timeline/01-college.jpg",
        "/static/images/timeline/02-friends.jpg",
        "/static/images/timeline/03-bestfriends.jpg",
        "/static/images/timeline/04-engagement.jpg",
        "/static/images/timeline/05-marriage.jpg",
        "/static/images/timeline/06-today.jpg",
    ]

    imgs = images + [None] * 10
    return [
        {
            "year": "School",
            "title": "Where we first crossed paths",
            "text": "We met in school, but back then we never really talked. Still, maybe life already knew something we did not.",
            "image": None,
        },
        {
            "year": "2013",
            "title": "College brought us together",
            "text": "In 2013, we met again in college. We became friends, and slowly something special started growing between us.",
            "image": imgs[0],
        },
        {
            "year": "Master’s",
            "title": "Best friends first",
            "text": "During our Master’s, our friendship became stronger. Somewhere between conversations and comfort, I started falling for you deeper and deeper.",
            "image": imgs[1],
        },
        {
            "year": "Proposal",
            "title": "Finally yes ❤️",
            "text": "In our story, I was the one who proposed — not once, but many times — and finally you said yes.",
            "image": imgs[2],
        },
        {
            "year": "2022",
            "title": "Engagement 💍",
            "text": "One of the happiest chapters of our life began when we got engaged.",
            "image": imgs[3],
        },
        {
            "year": "2023",
            "title": "Marriage ❤️",
            "text": "We got married and promised to walk together through every up and down.",
            "image": imgs[4],
        },
        {
            "year": "Today",
            "title": "Still choosing you",
            "text": "Today, I still choose you, pray for your dreams, and look forward to growing older with you.",
            "image": imgs[5],
        },
    ]


@app.route("/")
def home():
    hero_images = discover_files(STATIC_DIR / "images" / "hero", IMAGE_EXTS)
    timeline_images = discover_files(STATIC_DIR / "images" / "timeline", IMAGE_EXTS)
    final_image = discover_one(STATIC_DIR / "images" / "final", IMAGE_EXTS)
    video_url = discover_one(STATIC_DIR / "video", VIDEO_EXTS)
    audio_url = discover_one(STATIC_DIR / "audio", AUDIO_EXTS)

    data = {
        "title": "Happy Birthday My Love ❤️",
        "subtitle": "A little digital love story made only for you.",
        "countdown_start": 3,
        "memories": opening_memories(hero_images),
        # "birthday_story": [
        #     "Some people come into life quietly… and slowly become everything.",
        #     "Somewhere between friendship and love, you became my safest place.",
        #     "Being with you always felt natural, like something my heart already knew.",
        #     "Even before we were officially together, you always made me feel I belonged beside you.",
        #     "With you, I never had to pretend to be someone else. I could always just be myself.",
        #     "You stood beside me in moments that mattered the most and made difficult days feel lighter.",
        #     "You believed in me even when I doubted myself, and that changed me in ways I cannot explain.",
        #     "Life started feeling like home the day you truly became part of it.",
        #     "Every year with you feels like another beautiful chapter of the story I never want to end.",
        #     "On your birthday, I just want to say thank you for being you and for being mine.",
        #     "I loved you, I love you, and I will always love you ❤️",
        # ],
        "birthday_story": [

        "Some people come into life quietly and slowly become everything. Somewhere between friendship and love, you became my safest place without me even realizing when it happened. Being with you always felt natural, like something my heart already knew long before I understood it myself. Even before we were officially together, you always made me feel I belonged beside you.\n\n"

        "With you, I never had to pretend to be someone else. I could always just be myself, and that comfort is one of the most beautiful gifts you have given me. You stood beside me in moments that mattered the most, believed in me when I doubted myself, and made difficult days feel lighter just by being there.\n\n"

        "Life started feeling like home the day you truly became part of it. Somewhere along the way, without even noticing, you became my strength, my peace, and my favorite habit. Every year with you feels like another beautiful chapter of a story I never want to end, and I feel grateful every single day that I get to walk this journey with you.\n\n"

        "On your birthday, I just want to say thank you for being you and for being mine. I loved you, I love you, and I will always love you ❤️"

        ],
        "stats": [
            {"label": "Years together", "value": "14", "note": "and counting"},
            {"label": "Milestones together", "value": "Many", "note": "and still growing"},
            {"label": "Reasons I love you", "value": "Infinite ♾️", "note": "more every day"},
            {"label": "My forever person", "value": "You", "note": "always and always"},
        ],
        "happiness_labels": ["Friends", "Best Friends", "Proposal", "Engagement", "Marriage", "Today", "Forever"],
        "happiness_values": [12, 28, 46, 70, 88, 96, 100],
        "love_messages": [
            "You are my safest place and my favorite person in the world ❤️",
            "Life started feeling like home the day you came into it",
            "Loving you is the easiest and happiest thing I’ve ever done",
            "Every version of my future has you in it",
            "You are not just my husband, you are my best decision",
            "I still fall for you a little more every single day",
            "With you, forever still feels too short",
            "You are my peace in chaos and my smile in silence",
            "I didn’t just find love… I found my person",
            "Happy Birthday to the man who made my life beautiful ❤️",
            "I’m so lucky I get to celebrate you today and every day",
            "Today we celebrate you… my heart celebrates you every day",
            "Life with you is my favorite adventure",
            "You are my favorite notification in life",
            "Loving you is my full-time job",
            "You are my daily dose of happiness",
            "You make my world brighter just by existing",
            "From the day I fell for you to today… my heart still chooses you",
            "Every memory with you is my treasure",
            "We didn’t just grow older together… we grew stronger together",
            "Thank you for walking every step of life with me",
        ],
        "quiz": [
            {
                "question": "Where did our story truly begin to unfold?",
                "options": ["School", "College", "At a cafe"],
                "answer": 1,
                "response": "Yes ❤️ College is where our real story started opening up.",
            },
            {
                "question": "Who kept proposing in our love story?",
                "options": ["You", "Me", "Both together"],
                "answer": 1,
                "response": "Correct 😄 I was the one who kept proposing until I finally got my yes.",
            },
            {
                "question": "Which year became our forever year?",
                "options": ["2021", "2022", "2023"],
                "answer": 2,
                "response": "Exactly ❤️ 2023 became our forever year.",
            },
        ],
        "timeline": timeline_items(timeline_images),
        "special_memories": [
            {
                "title": "Your first bike",
                "text": "When you bought your first bike during MSc, I was the one you wanted to sit first on it. That moment stayed with me in a special way.",
            },
            {
                "title": "Your first home",
                "text": "When you were getting the documents for your first self-owned house, you wanted me there beside you. That made me feel I already had a place in your life.",
            },
            {
                "title": "The gift I never forgot",
                "text": "One birthday, you gave me something special. It wasn't just a gift — it was the first time you had ever given something so special to someone, and the fact that you chose me made it unforgettable..",
            },
            {
                "title": "My biggest supporter",
                "text": "You stood beside me while I was preparing for my first job and helped me believe in myself.",
            },
        ],
        "admire_lines": [
            "There are so many things I admire about you.",
            "I love how naturally you care for everyone around you and help people without expecting anything in return.",
            "I love how you treat my parents as your own and never made me feel they were anything less important.",
            "Even when we argue, and even when I am upset, you still try to lift my mood and make me smile again.",
            "I love the child in you — the softness with which you want to be loved and cared for.",
            "There are so many reasons I love you, and honestly, I love everything about you.",
            "I love you to the moon and back ❤️",
        ],
        "video_url": video_url,
        "audio_url": audio_url,
        "date_plan": {
        "title": "Birthday surprise unlocked just for you ❤️",
        "movie": "Your birthday celebration",
        "when": "This Saturday",
        "detail": "The plan you made for us ❤️",
        "secret": "A surprise waiting for me too ✨",
        "note": """I wanted to surprise you, But since you have meetings on your birthday, we'll celebrate it on Saturday instead.

        Usually, the birthday person is the one who gets surprised… but with us it's a little different. This time, the birthday boy himself already planned the dinner and chose the place just to surprise me — and honestly, that made me smile even more.

        So until then, consider this my small birthday surprise for you… and Saturday is my official chance to steal you away properly 😊"""
        },
        "closing_note": {
            "title": "And just like that…",
            "lines": [
                "From school days, to friendship, to love, to forever — you became my favorite part of life.",
                "Thank you for being my person, my peace, and my home.",
                "Happy Birthday once again, my love ❤️",
                "Our best chapters are still waiting for us.",
            ],
        },
        "final_image": final_image,
    }
    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
