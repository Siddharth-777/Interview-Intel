import random

from scripts.seed_data.companies import TOPIC_YEAR_BIAS
from scripts.seed_data.questions import QUESTION_POOLS

STYLES = ["casual", "formal", "bullet", "messy"]

# ── Random detail pools ──────────────────────────────────────────────

DURATIONS = [
    "20 minutes",
    "25 minutes",
    "30 minutes",
    "30-40 minutes",
    "45 minutes",
    "about an hour",
    "1 hour",
    "1.5 hours",
    "2 hours",
]
DIFFICULTIES = [
    "easy",
    "moderate",
    "medium",
    "medium-hard",
    "hard",
    "tricky",
    "manageable",
    "challenging",
    "not too bad",
    "fairly tough",
]
INTERVIEWER_ADJS = [
    "friendly",
    "nice",
    "strict but fair",
    "professional",
    "helpful",
    "calm",
    "senior",
    "very experienced",
    "encouraging",
    "straightforward",
]
OUTCOMES = [
    "Selected",
    "Rejected after final round",
    "Waitlisted",
    "Got the offer",
    "Did not clear",
    "Selected - joined",
    "Rejected at technical round",
    "Offer received after 2 weeks",
]
FEELINGS = [
    "decent",
    "pretty good",
    "tough but fair",
    "straightforward",
    "intense",
    "smooth",
    "okay",
    "challenging overall",
    "better than expected",
]
TIPS = [
    "Focus on DSA fundamentals and practice on LeetCode/GFG",
    "Practice SQL queries daily, especially joins and subqueries",
    "Be thorough with OOP concepts and design patterns",
    "Prepare system design basics even for fresher roles",
    "Aptitude practice is key - use IndiaBix or PrepInsta",
    "Be confident in the HR round, have STAR-method answers ready",
    "Revise OS and networking basics from Gate Smashers or Neso Academy",
    "Practice mock interviews with friends or Pramp",
    "Focus on clean code and explain your thought process aloud",
    "Don't just memorize - understand the WHY behind each concept",
    "Time management during the online test is crucial",
    "Go through Glassdoor and GeeksforGeeks for company-specific questions",
]
TIMEFRAMES = [
    "a week",
    "10 days",
    "about 2 weeks",
    "2 weeks",
    "3 weeks",
    "about a month",
    "within 5 days",
]
TANGENTIAL = [
    "The campus placement cell organized it really well.",
    "Internet was flaky during the online round which stressed me out.",
    "They had a nice office btw.",
    "There were around 200 students sitting for the first round.",
    "The interviewers were running late by almost an hour.",
    "I prepared mostly from GeeksforGeeks and InterviewBit.",
    "Waited in the lobby for like 2 hours before my turn.",
    "They offered tea/coffee before the interview which was nice.",
    "",
    "",
    "",
]

# ── Intro templates ──────────────────────────────────────────────────

INTRO_TEMPLATES: dict[str, list[str]] = {
    "casual": [
        (
            "Hey everyone! I recently interviewed at {company}"
            " for the {role} position ({year}). Here's my experience:"
        ),
        "Sharing my {company} interview experience"
        " for {role} role. This was in {year}.",
        (
            "So I gave my interview at {company} for the {role}"
            " position in {year}. The whole process had"
            " {num_rounds} rounds. Let me share how it went."
        ),
        (
            "Just finished my {company} interview process"
            " ({role}, {year}). Thought I'd share for"
            " anyone who's preparing!"
        ),
    ],
    "formal": [
        (
            "I attended the interview process at {company}"
            " for the position of {role} in {year}. The"
            " selection procedure comprised {num_rounds} rounds."
        ),
        (
            "I would like to share my interview experience at"
            " {company} for the {role} role ({year}). The"
            " recruitment process consisted of"
            " {num_rounds} stages."
        ),
        (
            "The following is an account of my interview at"
            " {company} for {role} ({year}). The process"
            " involved {num_rounds} rounds of evaluation."
        ),
    ],
    "bullet": [
        "Company: {company}\nRole: {role}\nYear: {year}"
        "\nTotal Rounds: {num_rounds}\n\nInterview Process:",
        "**{company} - {role} Interview Experience ({year})**"
        "\nRounds: {num_rounds}\n\nBreakdown:",
    ],
    "messy": [
        "heyy guys so i gave my {company} interview"
        " for {role} in {year}. sharing my experiance here",
        (
            "guys just completed the {company} interview"
            " process, {role} role ({year})."
            " here goes my experience"
        ),
        (
            "my {company} intervew experience for {role}"
            " position, {year}. {num_rounds} rounds total."
            " hope this helsp someone!"
        ),
    ],
}

# ── Round templates ──────────────────────────────────────────────────

ROUND_TEMPLATES: dict[str, list[str]] = {
    "casual": [
        (
            "Round {idx} - {round_name} ({duration}):"
            " {questions_text}. The interviewer was {adj}"
            " and I found it {difficulty}. {tangential}"
        ),
        (
            "Next was the {round_name}, lasted about"
            " {duration}. They asked me {questions_text}."
            " Difficulty-wise it was {difficulty}."
            " {tangential}"
        ),
        (
            "The {round_name} went for around {duration}."
            " Questions covered: {questions_text}."
            " I'd say it was {difficulty}. {tangential}"
        ),
    ],
    "formal": [
        (
            "Round {idx} ({round_name}): This round lasted"
            " approximately {duration}. The questions posed"
            " included {questions_text}. The difficulty"
            " level was {difficulty}."
        ),
        (
            "The {round_name} spanned {duration}. I was"
            " evaluated on: {questions_text}. Overall, the"
            " round was {difficulty} in difficulty."
        ),
        (
            "In the {round_name} ({duration}), the"
            " interviewer assessed the following areas:"
            " {questions_text}. The round was {difficulty}."
        ),
    ],
    "bullet": [
        "**Round {idx}: {round_name}** ({duration})"
        "\n- Difficulty: {difficulty}"
        "\n- Questions:\n{questions_bullet}",
        "Round {idx} - {round_name}"
        "\n  Duration: {duration}"
        "\n  Difficulty: {difficulty}"
        "\n  Topics:\n{questions_bullet}",
    ],
    "messy": [
        (
            "round {idx} - {round_name} ({duration})."
            " they askd about {questions_text}."
            " was {difficulty} tbh. {tangential}"
        ),
        (
            "{round_name} next, around {duration}."
            " questons were: {questions_text}."
            " {difficulty} overall"
        ),
        (
            "then {round_name} for like {duration}.."
            " {questions_text}."
            " i found it {difficulty}. {tangential}"
        ),
    ],
}

# ── Outro templates ──────────────────────────────────────────────────

OUTRO_TEMPLATES: dict[str, list[str]] = {
    "casual": [
        (
            "Overall it was a {feeling} experience."
            " The result came in {timeframe}."
            " My tip: {tip}. Good luck everyone!"
        ),
        (
            "That's it! The whole process was {feeling}."
            " Heard back in {timeframe}. Hope this helps!"
        ),
        (
            "Final verdict: {outcome}. {feeling} overall."
            " If you're preparing, I'd suggest: {tip}."
        ),
    ],
    "formal": [
        (
            "In summary, the process was {feeling}."
            " The outcome ({outcome}) was communicated"
            " within {timeframe}. I would recommend"
            " candidates to {tip}."
        ),
        (
            "Overall, the interview experience was"
            " {feeling}. Result: {outcome}."
            " Preparation advice: {tip}."
        ),
    ],
    "bullet": [
        "\nResult: {outcome}\nOverall Difficulty:"
        " {feeling}\nResponse Time:"
        " {timeframe}\nPrep Tips: {tip}",
        "\nVerdict: {outcome}"
        "\nExperience: {feeling}\nTip: {tip}",
    ],
    "messy": [
        (
            "overal it was {feeling}."
            " result: {outcome}. took {timeframe}."
            " my tip - {tip}. hope this helsp!!"
        ),
        (
            "thats my experience. {feeling}."
            " {outcome}. heard back in {timeframe}."
            " best of luck guys!!"
        ),
    ],
}


# ── Core functions ───────────────────────────────────────────────────


def pick_questions(
    topics: list[str],
    q_count: tuple[int, int],
    rng: random.Random,
    year: int = 2024,
) -> list[str]:
    """Pick q_count questions from the given topics, weighted by popularity and year trend."""
    n = rng.randint(q_count[0], q_count[1])
    selected: list[str] = []
    for _ in range(n):
        topic_weights = []
        for t in topics:
            bias = TOPIC_YEAR_BIAS.get(t, {}).get(year, 1.0)
            topic_weights.append(bias)
        topic = rng.choices(topics, weights=topic_weights, k=1)[0]
        pool = QUESTION_POOLS[topic]

        group_weights = [w for w, _ in pool]
        group = rng.choices(pool, weights=group_weights, k=1)[0]
        phrasing = rng.choice(group[1])
        selected.append(phrasing)
    return selected


def _format_questions_inline(questions: list[str], rng: random.Random) -> str:
    if len(questions) == 1:
        return questions[0]
    if len(questions) == 2:
        return f"{questions[0]} and {questions[1]}"
    joined = ", ".join(questions[:-1])
    conj = rng.choice([" and ", " and also ", ", plus "])
    return joined + conj + questions[-1]


def _format_questions_bullet(questions: list[str]) -> str:
    return "\n".join(f"  * {q}" for q in questions)


def _format_round(
    round_info: dict,
    idx: int,
    style: str,
    rng: random.Random,
    year: int,
) -> str:
    questions = pick_questions(round_info["topics"], round_info["q_count"], rng, year)
    template = rng.choice(ROUND_TEMPLATES[style])

    questions_text = _format_questions_inline(questions, rng)
    questions_bullet = _format_questions_bullet(questions)
    tangential = rng.choice(TANGENTIAL)

    return template.format(
        idx=idx,
        round_name=round_info["name"],
        duration=rng.choice(DURATIONS),
        difficulty=rng.choice(DIFFICULTIES),
        adj=rng.choice(INTERVIEWER_ADJS),
        questions_text=questions_text,
        questions_bullet=questions_bullet,
        tangential=tangential,
    )


def assemble_narrative(
    company: str,
    role: str,
    year: int,
    rounds: list[dict],
    rng: random.Random,
    style: str | None = None,
) -> str:
    """Build a complete interview experience narrative from templates."""
    if style is None:
        style = rng.choice(STYLES)

    parts: list[str] = []

    intro = rng.choice(INTRO_TEMPLATES[style]).format(
        company=company,
        role=role,
        year=year,
        num_rounds=len(rounds),
    )
    parts.append(intro)

    for idx, round_info in enumerate(rounds, 1):
        parts.append(_format_round(round_info, idx, style, rng, year))

    outro = rng.choice(OUTRO_TEMPLATES[style]).format(
        feeling=rng.choice(FEELINGS),
        outcome=rng.choice(OUTCOMES),
        timeframe=rng.choice(TIMEFRAMES),
        tip=rng.choice(TIPS),
    )
    parts.append(outro)

    return "\n\n".join(parts)
