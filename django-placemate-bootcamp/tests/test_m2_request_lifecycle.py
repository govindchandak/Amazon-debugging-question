"""Mission 2 – Django request lifecycle: URL -> view -> response."""
import pytest


@pytest.mark.django_db
class TestMission2RequestLifecycle:

    def test_list_drives_returns_json_array(self, anonymous, make_drive):
        make_drive('Zoho', days_left=2)
        make_drive('Amazon', days_left=1)
        make_drive('Closed Co', status='CLOSED')
        response = anonymous.get('/api/drives/')
        assert response.status_code == 200
        assert [d['company'] for d in response.json()] == ['Amazon', 'Zoho']

    def test_drive_detail_by_id(self, anonymous, make_drive):
        drive = make_drive('Amazon', role='SDE I')
        response = anonymous.get(f'/api/drives/{drive.id}')
        assert response.status_code == 200
        assert response.json()['drive']['role'] == 'SDE I'

    def test_save_a_drive(self, make_student, make_drive):
        api, _ = make_student('21CS001')
        drive = make_drive('Amazon')
        response = api.post(f'/api/drives/{drive.id}/save')
        assert response.status_code == 201
        assert response.json()['message'] == 'Drive saved'

    def test_unsave_a_drive_with_delete(self, make_student, make_drive):
        api, _ = make_student('21CS001')
        drive = make_drive('Amazon')
        api.post(f'/api/drives/{drive.id}/save')
        response = api.delete(f'/api/drives/{drive.id}/save')
        assert response.status_code == 200
        assert response.json()['message'] == 'Drive removed from saved list'

    def test_add_note_reads_json_body(self, make_student, make_drive):
        api, _ = make_student('21CS001')
        drive = make_drive('Amazon')
        response = api.post(f'/api/drives/{drive.id}/notes', {'note': 'Revise graphs'})
        assert response.status_code == 201
        assert response.json()['note']['text'] == 'Revise graphs'
