"""Transform O*NET source files into Phase 1 CSV deliverables."""

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
IMPORTANCE_THRESHOLD = 3.5
MAX_SOFTWARE_SKILLS_PER_ROLE = 25


def load_source_files() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    occupations = pd.read_csv(DATA_DIR / "occupation_data.csv")
    essential = pd.read_csv(DATA_DIR / "essential_skills.csv")
    transferable = pd.read_csv(DATA_DIR / "transferable_skills.csv")
    software = pd.read_csv(DATA_DIR / "software_skills.csv")
    return occupations, essential, transferable, software


def important_skills(skills_df: pd.DataFrame, soc_code: str) -> list[str]:
    subset = skills_df[
        (skills_df["O*NET-SOC Code"] == soc_code)
        & (skills_df["Scale Name"] == "Importance")
        & (skills_df["Data Value"] >= IMPORTANCE_THRESHOLD)
    ]
    return subset["Element Name"].dropna().unique().tolist()


def software_skills_for_role(software_df: pd.DataFrame, soc_code: str) -> list[str]:
    subset = software_df[software_df["O*NET-SOC Code"] == soc_code]
    hot = subset[subset["Hot Technology"] == "Y"]["Workplace Example"]
    other = subset[subset["Hot Technology"] != "Y"]["Workplace Example"]
    combined = pd.concat([hot, other]).dropna().unique().tolist()
    return combined[:MAX_SOFTWARE_SKILLS_PER_ROLE]


def build_skills_csv(
    essential: pd.DataFrame,
    transferable: pd.DataFrame,
    software: pd.DataFrame,
) -> pd.DataFrame:
    all_skills = set()
    all_skills.update(essential["Element Name"].dropna().unique())
    all_skills.update(transferable["Element Name"].dropna().unique())
    all_skills.update(software["Workplace Example"].dropna().unique())
    all_skills.update(software["Element Name"].dropna().unique())
    return pd.DataFrame({"skill": sorted(all_skills)})


def build_careers_csv(
    occupations: pd.DataFrame,
    essential: pd.DataFrame,
    transferable: pd.DataFrame,
    software: pd.DataFrame,
) -> pd.DataFrame:
    careers = []
    for _, row in occupations.iterrows():
        soc_code = row["O*NET-SOC Code"]
        skills = set(important_skills(essential, soc_code))
        skills.update(important_skills(transferable, soc_code))
        skills.update(software_skills_for_role(software, soc_code))

        careers.append(
            {
                "role": row["Title"],
                "description": row["Description"],
                "required_skills": ", ".join(sorted(skills)),
            }
        )
    return pd.DataFrame(careers)


def build_courses_csv(skills_df: pd.DataFrame) -> pd.DataFrame:
    """Seed learning resources for high-value skills (synthetic catalog)."""
    priority_skills = [
        "Python",
        "SQL",
        "Machine Learning",
        "JavaScript",
        "Project Management",
        "Data Analysis",
        "Cloud Computing",
        "Communication",
        "Critical Thinking",
        "Java",
    ]
    available = set(skills_df["skill"].str.lower())
    selected = [s for s in priority_skills if s.lower() in available]
    if not selected:
        selected = skills_df["skill"].head(10).tolist()

    templates = [
        ("Intro to {skill}", "https://www.coursera.org", "beginner", 10),
        ("{skill} Fundamentals", "https://www.udemy.com", "beginner", 8),
        ("Advanced {skill}", "https://www.edx.org", "advanced", 20),
        ("{skill} for Professionals", "https://www.linkedin.com/learning", "intermediate", 12),
    ]

    courses = []
    for skill in selected:
        for idx, (title_tpl, url, level, hours) in enumerate(templates):
            courses.append(
                {
                    "title": title_tpl.format(skill=skill),
                    "url": url,
                    "skill_taught": skill,
                    "level": level,
                    "duration_hours": hours + idx * 2,
                }
            )
    return pd.DataFrame(courses)


def main() -> None:
    occupations, essential, transferable, software = load_source_files()

    skills_df = build_skills_csv(essential, transferable, software)
    careers_df = build_careers_csv(occupations, essential, transferable, software)
    courses_df = build_courses_csv(skills_df)

    skills_df.to_csv(DATA_DIR / "skills.csv", index=False)
    careers_df.to_csv(DATA_DIR / "careers.csv", index=False)
    courses_df.to_csv(DATA_DIR / "courses.csv", index=False)

    print(f"Wrote {len(skills_df)} skills -> data/skills.csv")
    print(f"Wrote {len(careers_df)} careers -> data/careers.csv")
    print(f"Wrote {len(courses_df)} courses -> data/courses.csv")


if __name__ == "__main__":
    main()
