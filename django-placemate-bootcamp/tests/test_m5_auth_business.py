"""Mission 5 – authentication, authorisation and business rules."""
import pytest


@pytest.mark.django_db
class TestMission5AuthAndBusinessLogic:

    def test_eligibility_needs_login(self, anonymous, make_drive):
        drive = make_drive('Amazon')
        response = anonymous.get(f'/api/drives/{drive.id}/eligibility')
        assert response.status_code == 401

    def test_only_tpo_can_close_a_drive(self, make_student, tpo, make_drive):
        api, _ = make_student('21CS001')
        drive = make_drive('Amazon')
        assert api.post(f'/api/drives/{drive.id}/close').status_code == 403
        assert tpo.post(f'/api/drives/{drive.id}/close').status_code == 200

    def test_cgpa_equal_to_cutoff_is_eligible(self, make_student, make_drive):
        api, _ = make_student('21CS001', cgpa=7.5)
        drive = make_drive('Amazon', min_cgpa=7.5)
        body = api.get(f'/api/drives/{drive.id}/eligibility').json()
        assert body['eligible'] is True
        assert body['reasons'] == []

    def test_backlogs_equal_to_limit_are_allowed(self, make_student, make_drive):
        api, _ = make_student('21CS001', backlogs=1)
        drive = make_drive('TCS', max_backlogs=1)
        assert api.get(f'/api/drives/{drive.id}/eligibility').json()['eligible'] is True

    def test_branch_match_ignores_case(self, make_student, make_drive):
        api, _ = make_student('21IT014', branch='it')
        drive = make_drive('Zoho', branches=['CSE', 'IT'])
        assert api.get(f'/api/drives/{drive.id}/eligibility').json()['eligible'] is True
