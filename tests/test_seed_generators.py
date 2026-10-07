import random

from scripts.seed_data.companies import COMPANIES, ROLES
from scripts.seed_data.narratives import (
    STYLES,
    assemble_narrative,
    pick_questions,
)
from scripts.seed_data.questions import QUESTION_POOLS
from scripts.seed_synthetic_data import build_experiences


class TestQuestionPools:
    def test_all_topics_have_entries(self):
        for topic, groups in QUESTION_POOLS.items():
            assert len(groups) >= 3, f"Topic '{topic}' has fewer than 3 question groups"

    def test_each_group_has_multiple_phrasings(self):
        for topic, groups in QUESTION_POOLS.items():
            for weight, phrasings in groups:
                assert weight >= 1
                assert len(phrasings) >= 2, (
                    f"Topic '{topic}' has a group with fewer than 2 phrasings"
                )

    def test_no_empty_question_strings(self):
        for topic, groups in QUESTION_POOLS.items():
            for _, phrasings in groups:
                for p in phrasings:
                    assert p.strip(), f"Empty phrasing in topic '{topic}'"


class TestPickQuestions:
    def test_returns_correct_count_range(self):
        rng = random.Random(1)
        for _ in range(50):
            qs = pick_questions(["dsa", "sql"], (2, 4), rng)
            assert 2 <= len(qs) <= 4

    def test_returns_strings(self):
        rng = random.Random(2)
        qs = pick_questions(["oop"], (3, 3), rng)
        assert all(isinstance(q, str) and len(q) > 5 for q in qs)

    def test_different_seeds_give_different_results(self):
        qs1 = pick_questions(["dsa"], (5, 5), random.Random(10))
        qs2 = pick_questions(["dsa"], (5, 5), random.Random(99))
        assert qs1 != qs2

    def test_all_topics_produce_questions(self):
        rng = random.Random(3)
        for topic in QUESTION_POOLS:
            qs = pick_questions([topic], (1, 1), rng)
            assert len(qs) == 1
            assert isinstance(qs[0], str)


class TestCompanyConfigs:
    def test_all_companies_have_required_fields(self):
        for name, cfg in COMPANIES.items():
            assert "rounds" in cfg, f"{name} missing rounds"
            assert "count" in cfg, f"{name} missing count"
            assert "role_weights" in cfg, f"{name} missing role_weights"
            assert "year_weights" in cfg, f"{name} missing year_weights"

    def test_round_topics_exist_in_pools(self):
        for name, cfg in COMPANIES.items():
            for rnd in cfg["rounds"]:
                for topic in rnd["topics"]:
                    assert topic in QUESTION_POOLS, (
                        f"{name} round '{rnd['name']}' references unknown topic '{topic}'"
                    )

    def test_total_count_around_200(self):
        total = sum(cfg["count"] for cfg in COMPANIES.values())
        assert 190 <= total <= 210, f"Total experience count is {total}, expected ~200"

    def test_razorpay_has_few_experiences(self):
        assert COMPANIES["Razorpay"]["count"] == 2

    def test_roles_in_weights_are_valid(self):
        for name, cfg in COMPANIES.items():
            for role in cfg["role_weights"]:
                assert role in ROLES, f"{name} has unknown role '{role}'"


class TestAssembleNarrative:
    def test_produces_nonempty_text(self):
        rng = random.Random(42)
        cfg = COMPANIES["TCS"]
        text = assemble_narrative("TCS", "SDE", 2024, cfg["rounds"], rng)
        assert len(text) > 100

    def test_contains_company_and_role(self):
        rng = random.Random(42)
        cfg = COMPANIES["Amazon"]
        text = assemble_narrative("Amazon", "Backend", 2023, cfg["rounds"], rng)
        assert "Amazon" in text
        assert "Backend" in text

    def test_all_styles_produce_output(self):
        for style in STYLES:
            rng = random.Random(7)
            cfg = COMPANIES["Zoho"]
            text = assemble_narrative("Zoho", "SDE", 2024, cfg["rounds"], rng, style=style)
            assert len(text) > 50, f"Style '{style}' produced too-short output"

    def test_deterministic_with_same_seed(self):
        cfg = COMPANIES["Infosys"]
        t1 = assemble_narrative("Infosys", "QA", 2023, cfg["rounds"], random.Random(5))
        t2 = assemble_narrative("Infosys", "QA", 2023, cfg["rounds"], random.Random(5))
        assert t1 == t2


class TestBuildExperiences:
    def test_correct_total_count(self):
        rng = random.Random(42)
        exps = build_experiences(rng)
        expected = sum(cfg["count"] for cfg in COMPANIES.values())
        assert len(exps) == expected

    def test_all_companies_represented(self):
        rng = random.Random(42)
        exps = build_experiences(rng)
        companies = {e["company"] for e in exps}
        assert companies == set(COMPANIES.keys())

    def test_experiences_have_required_fields(self):
        rng = random.Random(42)
        exps = build_experiences(rng)
        for exp in exps:
            assert "company" in exp
            assert "role" in exp
            assert "year" in exp
            assert "raw_text" in exp
            assert len(exp["raw_text"]) > 50

    def test_no_two_narratives_identical(self):
        rng = random.Random(42)
        exps = build_experiences(rng)
        texts = [e["raw_text"] for e in exps]
        assert len(set(texts)) == len(texts)

    def test_deterministic(self):
        e1 = build_experiences(random.Random(42))
        e2 = build_experiences(random.Random(42))
        assert [e["raw_text"] for e in e1] == [e["raw_text"] for e in e2]
