"""Mission 4 – Django ORM: filters, save(), get vs filter, annotate, ordering."""
import pytest

from applications.models import Application


@pytest.mark.django_db
class TestMission4Orm:

    def test_search_min_ctc_includes_equal(self, anonymous, make_drive):
        make_drive('Zoho', ctc=8.4)
        make_drive('Amazon', ctc=44.0)
        make_drive('Infosys', ctc=3.6)
        companies = {d['company'] for d in anonymous.get('/api/drives/search?minCtc=8.4').json()['drives']}
        assert companies == {'Zoho', 'Amazon'}

    def test_stats_count_only_active_applications(self, anonymous, make_student, make_drive, make_application):
        drive = make_drive('Amazon', min_cgpa=6.0)
        _, a = make_student('21CS001')
        _, b = make_student('21CS002')
        make_application(a, drive)
        make_application(b, drive, status='WITHDRAWN')
        stats = anonymous.get('/api/drives/stats').json()['stats']
        assert stats[0]['activeApplications'] == 1

    def test_withdraw_is_saved(self, make_student, make_drive, make_application):
        api, student = make_student('21CS001')
        drive = make_drive('Amazon')
        app_id = make_application(student, drive).id
        assert api.post(f'/api/applications/{app_id}/withdraw').status_code == 200
        assert Application.objects.get(id=app_id).status == 'WITHDRAWN'

    def test_someone_elses_application_is_404(self, make_student, make_drive, make_application):
        _, a = make_student('21CS001')
        api_b, _ = make_student('21CS002')
        drive = make_drive('Amazon')
        app_id = make_application(a, drive).id
        response = api_b.get(f'/api/applications/{app_id}')
        assert response.status_code == 404

    def test_my_applications_newest_first(self, make_student, make_drive, make_application):
        api, student = make_student('21CS001')
        make_application(student, make_drive('Zoho'))
        make_application(student, make_drive('Amazon'))
        companies = [a['company'] for a in api.get('/api/applications/me').json()['applications']]
        assert companies == ['Amazon', 'Zoho']
