"""Seed interview_experiences with ~200 synthetic narratives.

Usage:
    python -m scripts.seed_synthetic_data              # insert if table is empty
    python -m scripts.seed_synthetic_data --reset      # truncate & re-seed (with prompt)
    python -m scripts.seed_synthetic_data --no-llm     # skip Ollama paraphrase pass
"""

import argparse
import asyncio
import random
import sys
from collections import Counter
from pathlib import Path

import httpx
from sqlalchemy import func, select, text

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.config import settings
from app.core.db import async_session, engine
from app.models.experience import InterviewExperience
from scripts.seed_data.companies import COMPANIES
from scripts.seed_data.narratives import assemble_narrative

SEED = 42
LLM_PARAPHRASE_RATIO = 0.25


def build_experiences(rng: random.Random) -> list[dict]:
    """Generate all experience dicts (no DB, no LLM)."""
    experiences: list[dict] = []

    for company, cfg in COMPANIES.items():
        role_names = list(cfg["role_weights"].keys())
        role_weights = [cfg["role_weights"][r] for r in role_names]
        year_vals = list(cfg["year_weights"].keys())
        year_weights = [cfg["year_weights"][y] for y in year_vals]

        for _ in range(cfg["count"]):
            role = rng.choices(role_names, weights=role_weights, k=1)[0]
            year = rng.choices(year_vals, weights=year_weights, k=1)[0]
            narrative = assemble_narrative(
                company=company,
                role=role,
                year=year,
                rounds=cfg["rounds"],
                rng=rng,
            )
            experiences.append(
                {
                    "company": company,
                    "role": role,
                    "year": year,
                    "raw_text": narrative,
                }
            )

    rng.shuffle(experiences)
    return experiences


async def paraphrase_batch(
    experiences: list[dict],
    rng: random.Random,
) -> list[dict]:
    """Optionally paraphrase a subset of narratives via Ollama for extra variety."""
    indices = list(range(len(experiences)))
    rng.shuffle(indices)
    to_paraphrase = indices[: int(len(experiences) * LLM_PARAPHRASE_RATIO)]

    async with httpx.AsyncClient(timeout=90.0) as client:
        for i in to_paraphrase:
            try:
                resp = await client.post(
                    f"{settings.OLLAMA_BASE_URL}/api/generate",
                    json={
                        "model": settings.LLM_MODEL,
                        "prompt": (
                            "Rewrite the following interview experience post. "
                            "Keep ALL facts, questions, company name, role, and year "
                            "exactly the same. Just vary the wording slightly to sound "
                            "like a different person wrote it. Maintain the same tone. "
                            "Output ONLY the rewritten text.\n\n" + experiences[i]["raw_text"]
                        ),
                        "stream": False,
                    },
                )
                if resp.status_code == 200:
                    rewritten = resp.json().get("response", "").strip()
                    if len(rewritten) > 100:
                        experiences[i]["raw_text"] = rewritten
            except httpx.HTTPError:
                pass  # keep original on failure

    return experiences


async def seed(*, reset: bool, use_llm: bool) -> None:
    async with async_session() as session:
        count_result = await session.execute(select(func.count()).select_from(InterviewExperience))
        existing = count_result.scalar_one()

        if existing > 0 and not reset:
            print(f"Table already has {existing} rows. Use --reset to truncate and re-seed.")
            return

        if reset and existing > 0:
            confirm = input(
                f"This will DELETE all {existing} rows from interview_experiences. "
                "Type 'yes' to confirm: "
            )
            if confirm.strip().lower() != "yes":
                print("Aborted.")
                return
            await session.execute(text("TRUNCATE interview_experiences CASCADE"))
            await session.commit()
            print(f"Truncated {existing} rows.")

        rng = random.Random(SEED)
        print("Generating narratives...")
        experiences = build_experiences(rng)

        if use_llm:
            n = int(len(experiences) * LLM_PARAPHRASE_RATIO)
            print(f"Paraphrasing ~{n} narratives via Ollama...")
            experiences = await paraphrase_batch(experiences, rng)

        rows = [InterviewExperience(**exp) for exp in experiences]
        session.add_all(rows)
        await session.commit()

        # Summary
        companies = Counter(e["company"] for e in experiences)
        years = Counter(e["year"] for e in experiences)
        roles = Counter(e["role"] for e in experiences)

        print(f"\nInserted {len(experiences)} experiences.\n")
        print("Per company:")
        for c in sorted(companies):
            print(f"  {c:20s} {companies[c]:3d}")
        print("\nPer year:")
        for y in sorted(years):
            print(f"  {y}  {years[y]:3d}")
        print("\nPer role:")
        for r in sorted(roles):
            print(f"  {r:15s} {roles[r]:3d}")

    await engine.dispose()


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed synthetic interview data")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Truncate interview_experiences before seeding",
    )
    parser.add_argument(
        "--no-llm",
        action="store_true",
        help="Skip Ollama paraphrase pass (works fully offline)",
    )
    args = parser.parse_args()
    asyncio.run(seed(reset=args.reset, use_llm=not args.no_llm))


if __name__ == "__main__":
    main()
