def serialize_drive(drive):
    return {
        '_id': str(drive.id),
        'company': drive.company.name,
        'tier': drive.company.tier,
        'ctcLpa': drive.company.ctc_lpa,
        'role': drive.role,
        'branches': drive.branches,
        'minCgpa': drive.min_cgpa,
        'maxBacklogs': drive.max_backlogs,
        'requiredSkills': drive.required_skills,
        'seats': drive.seats,
        'deadline': drive.deadline.isoformat(),
        'status': drive.status,
    }
