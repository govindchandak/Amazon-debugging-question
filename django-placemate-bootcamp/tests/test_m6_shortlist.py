"""Mission 6 – practical challenge: GET /api/drives/<id>/shortlist (README, Mission 6)."""
import pytest

from applications.models import Application


def apply_with_score(student, drive, score, status='APPLIED'):
    return Application.objects.create(student=student, drive=drive, test_score=score, status=status).id


@pytest.mark.django_db
class TestMission6Shortlist:

    def test_no_applicants_message(self, tpo, make_drive):
        drive = make_drive('Amazon')
        body = tpo.get(f'/api/drives/{drive.id}/shortlist').json()
        assert body['message'] == 'No eligible applicants yet'
        assert body['shortlist'] == []

    def test_scores_and_ranking(self, tpo, make_student, make_drive):
        drive = make_drive('Amazon', min_cgpa=7.0, skills=['Python', 'SQL'], seats=5)
        _, a = make_student('21CS001', name='Asha', cgpa=8.0, skills=[{'name': 'Python', 'level': 4}])
        _, b = make_student('21CS002', name='Ben', cgpa=9.0, skills=[{'name': 'Python', 'level': 3}, {'name': 'SQL', 'level': 3}])
        _, c = make_student('21CS003', name='Chitra', cgpa=7.5, skills=[])
        apply_with_score(a, drive, 90)
        apply_with_score(b, drive, 70)
        apply_with_score(c, drive, None)          # no test score yet -> not ranked
        body = tpo.get(f'/api/drives/{drive.id}/shortlist').json()
        assert body['message'] == 'Shortlisted 2 of 2 eligible applicants'
        rows = body['shortlist']
        assert [r['name'] for r in rows] == ['Ben', 'Asha']
        assert rows[0]['score'] == pytest.approx(0.84, abs=1e-3)
        assert rows[1]['score'] == pytest.approx(0.78, abs=1e-3)
        assert rows[1]['matchedSkills'] == ['Python']

    def test_withdrawn_applications_are_ignored(self, tpo, make_student, make_drive):
        drive = make_drive('Amazon', min_cgpa=7.0)
        _, a = make_student('21CS001', name='Asha', cgpa=8.0)
        _, b = make_student('21CS002', name='Ben', cgpa=9.0)
        apply_with_score(a, drive, 60)
        apply_with_score(b, drive, 95, status='WITHDRAWN')
        rows = tpo.get(f'/api/drives/{drive.id}/shortlist').json()['shortlist']
        assert [r['name'] for r in rows] == ['Asha']

    def test_only_as_many_as_seats(self, tpo, make_student, make_drive):
        drive = make_drive('Zoho', min_cgpa=6.0, seats=3)
        for i, score in enumerate([50, 90, 70, 80, 60]):
            _, api = make_student(f'21CS10{i}', name=f'S{i}', cgpa=8.0)
            apply_with_score(api, drive, score)
        body = tpo.get(f'/api/drives/{drive.id}/shortlist').json()
        assert [r['name'] for r in body['shortlist']] == ['S1', 'S3', 'S2']
        assert body['message'] == 'Shortlisted 3 of 5 eligible applicants'

    def test_skill_match_ignores_case(self, tpo, make_student, make_drive):
        drive = make_drive('Amazon', min_cgpa=6.0, skills=['Python', 'SQL'])
        _, api = make_student('21CS001', cgpa=8.0, skills=[{'name': 'python', 'level': 3}, {'name': 'sql', 'level': 2}])
        apply_with_score(api, drive, 50)
        row = tpo.get(f'/api/drives/{drive.id}/shortlist').json()['shortlist'][0]
        assert row['matchedSkills'] == ['Python', 'SQL']
        assert row['score'] == pytest.approx(0.72, abs=1e-3)

    def test_ties_go_to_higher_cgpa_then_roll_number(self, tpo, make_student, make_drive):
        drive = make_drive('Amazon', min_cgpa=6.0)
        _, z = make_student('21CS009', name='Zoya', cgpa=8.0)
        _, a = make_student('21CS004', name='Arun', cgpa=8.0)
        _, m = make_student('21CS006', name='Meera', cgpa=8.5)
        apply_with_score(z, drive, 70)
        apply_with_score(a, drive, 70)
        apply_with_score(m, drive, 65)            # same total score as the others
        names = [r['name'] for r in tpo.get(f'/api/drives/{drive.id}/shortlist').json()['shortlist']]
        assert names == ['Meera', 'Arun', 'Zoya']

    def test_confirm_saves_the_shortlist(self, tpo, make_student, make_drive):
        drive = make_drive('Amazon', min_cgpa=6.0, seats=1)
        _, a = make_student('21CS001', cgpa=8.0)
        _, b = make_student('21CS002', cgpa=7.0)
        a_app = apply_with_score(a, drive, 90)
        b_app = apply_with_score(b, drive, 40)
        assert tpo.post(f'/api/drives/{drive.id}/shortlist/confirm').json()['count'] == 1
        assert Application.objects.get(id=a_app).status == 'SHORTLISTED'
        assert Application.objects.get(id=b_app).status == 'APPLIED'
