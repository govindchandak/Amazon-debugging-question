"""Mission 3 – views and services: status codes, error contract, response shape."""
import pytest


@pytest.mark.django_db
class TestMission3ViewsAndServices:

    def test_apply_returns_201_and_the_application(self, make_student, make_drive):
        api, _ = make_student('21CS001', cgpa=8.5)
        drive = make_drive('Amazon', role='SDE I', min_cgpa=7.0)
        response = api.post(f'/api/drives/{drive.id}/apply')
        assert response.status_code == 201
        body = response.json()
        assert body['message'] == 'Application submitted'
        assert body['application']['company'] == 'Amazon'
        assert body['application']['status'] == 'APPLIED'

    def test_second_apply_is_409_already_applied(self, make_student, make_drive):
        api, _ = make_student('21CS001', cgpa=8.5)
        drive = make_drive('Amazon', min_cgpa=7.0)
        api.post(f'/api/drives/{drive.id}/apply')
        response = api.post(f'/api/drives/{drive.id}/apply')
        assert response.status_code == 409
        assert response.json()['error'] == 'ALREADY_APPLIED'

    def test_my_applications_use_camel_case(self, make_student, make_drive):
        api, _ = make_student('21CS001', cgpa=8.5)
        drive = make_drive('Amazon', min_cgpa=7.0)
        api.post(f'/api/drives/{drive.id}/apply')
        item = api.get('/api/applications/me').json()['applications'][0]
        assert set(item) == {'_id', 'driveId', 'company', 'role', 'status', 'appliedAt'}

    def test_not_eligible_is_422_with_reason(self, make_student, make_drive):
        api, _ = make_student('21CS001', cgpa=6.0)
        drive = make_drive('Amazon', min_cgpa=7.5)
        response = api.post(f'/api/drives/{drive.id}/apply')
        assert response.status_code == 422
        assert response.json()['error'] == 'NOT_ELIGIBLE'
        assert 'CGPA' in response.json()['message']
