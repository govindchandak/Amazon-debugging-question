"""
Mission 1 – Python essentials.

Helpers that build the student's profile summary card.
"""

READINESS_BANDS = [(8.0, 'A'), (7.0, 'B'), (6.0, 'C')]


def average_test_score(scores):
    """Average of the mock-test percentages, rounded to 1 decimal place. None when there are no scores."""
    if not scores:
        return None
    return round(sum(scores) // len(scores), 1)


def top_skills(skills, limit=3):
    """Skill names, highest level first; equal levels in alphabetical order."""
    ordered = sorted(skills, key=lambda s: (s['level'], s['name'].lower()), reverse=True)
    return [s['name'] for s in ordered[:limit]]


def skill_tags(skills, tags=[]):
    """Short tags for the card, e.g. ['#python', '#sql']. Duplicates (any case) appear once."""
    for skill in skills:
        tag = '#' + skill['name'].strip().lower().replace(' ', '-')
        if tag not in tags:
            tags.append(tag)
    return tags


def sorted_target_ctcs(target_ctcs):
    """Dream packages (stored as text) as numbers, highest first."""
    return sorted(target_ctcs, reverse=True)


def readiness_band(cgpa):
    for cutoff, band in READINESS_BANDS:
        if cgpa >= cutoff:
            return band
    return 'D'


def build_summary(student):
    band = readiness_band(student.cgpa)
    return {
        'name': student.name,
        'rollNo': student.roll_no,
        'cgpa': student.cgpa,
        'averageTestScore': average_test_score(student.test_scores),
        'topSkills': top_skills(student.skills),
        'tags': skill_tags(student.skills),
        'targetCtcs': sorted_target_ctcs(student.target_ctcs),
        'band': band,
        'dreamReady': band == 'A' or 'B',
    }
