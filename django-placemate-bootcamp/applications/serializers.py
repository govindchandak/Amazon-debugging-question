def serialize_application(application):
    return {
        '_id': str(application.id),
        'driveId': str(application.drive_id),
        'company': application.drive.company.name,
        'role': application.drive.role,
        'status': application.status,
        'applied_at': application.applied_at.isoformat(),
    }
