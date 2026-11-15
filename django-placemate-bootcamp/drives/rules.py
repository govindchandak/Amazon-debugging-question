"""
Mission 5 – business rules shared by apply, eligibility and shortlist.

A student is eligible for a drive when ALL of these hold:
  * the student's branch is one of drive.branches (case does not matter)
  * cgpa >= drive.min_cgpa
  * backlogs <= drive.max_backlogs
"""


def profile_reasons(student, drive):
    """Reasons the student's PROFILE does not meet the drive criteria ([] = eligible)."""
    reasons = []
    allowed = [b.upper() for b in drive.branches]
    if student.branch not in drive.branches:
        reasons.append(f'Branch {student.branch} is not allowed')
    if student.cgpa <= drive.min_cgpa:
        reasons.append(f'CGPA {student.cgpa} is below {drive.min_cgpa}')
    if student.backlogs >= drive.max_backlogs:
        reasons.append(f'{student.backlogs} backlogs, at most {drive.max_backlogs} allowed')
    return reasons
