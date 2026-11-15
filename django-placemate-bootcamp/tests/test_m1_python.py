"""Mission 1 – Python essentials. Endpoint: GET /api/students/me/summary"""
import pytest

URL = '/api/students/me/summary'


@pytest.mark.django_db
class TestMission1PythonEssentials:

    def test_average_test_score_keeps_decimals(self, make_student):
        api, _ = make_student('21CS001', test_scores=[70, 75])
        summary = api.get(URL).json()['summary']
        assert summary['averageTestScore'] == 72.5

    def test_tags_belong_only_to_the_student(self, make_student):
        api_a, _ = make_student('21CS001', skills=[{'name': 'Python', 'level': 4}])
        api_b, _ = make_student('21CS002', skills=[{'name': 'Java', 'level': 3}, {'name': 'java', 'level': 2}])
        assert api_a.get(URL).json()['summary']['tags'] == ['#python']
        assert api_b.get(URL).json()['summary']['tags'] == ['#java']

    def test_target_ctcs_are_numbers_highest_first(self, make_student):
        api, _ = make_student('21CS001', target_ctcs=['12.5', '9', '45'])
        assert api.get(URL).json()['summary']['targetCtcs'] == [45.0, 12.5, 9.0]

    def test_dream_ready_is_a_boolean(self, make_student):
        api, _ = make_student('21CS001', cgpa=6.4)
        summary = api.get(URL).json()['summary']
        assert summary['band'] == 'C'
        assert summary['dreamReady'] is False

    def test_top_skills_highest_level_then_alphabetical(self, make_student):
        skills = [{'name': 'SQL', 'level': 3}, {'name': 'Django', 'level': 3}, {'name': 'Python', 'level': 5}, {'name': 'Git', 'level': 1}]
        api, _ = make_student('21CS001', skills=skills)
        assert api.get(URL).json()['summary']['topSkills'] == ['Python', 'Django', 'SQL']
