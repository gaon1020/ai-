
import pytest
from week11.load_scores import load_scores


# 정상 데이터 테스트
def test_normal_data(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n"
        "김철수,80\n"
        "이영희,95\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [("김철수", 80), ("이영희", 95)]
    assert skipped == []


# 헤더만 있는 파일 테스트
def test_header_only(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text("name,score\n", encoding="utf-8")

    kept, skipped = load_scores(file)

    assert kept == []
    assert skipped == []


# 점수 경계값 테스트
def test_score_boundary(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n"
        "A,0\n"
        "B,100\n"
        "C,-1\n"
        "D,101\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [("A", 0), ("B", 100)]
    assert len(skipped) == 2
    assert skipped[0][2] == "점수가 0~100 밖"
    assert skipped[1][2] == "점수가 0~100 밖"


# 점수가 비어 있거나 문자인 경우
def test_invalid_scores(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n"
        "김철수,\n"
        "이영희,abc\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == []
    assert skipped[0][2] == "점수가 비어 있음"
    assert skipped[1][2] == "점수가 정수가 아님"


# 이름이 비어 있는 경우
def test_empty_name(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n"
        ",90\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == []
    assert skipped == [(2, ",90", "이름이 비어 있음")]


# 열 개수가 잘못된 경우
def test_wrong_columns(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n"
        "김철수,80,추가\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == []
    assert skipped[0][2] == "열 개수가 2가 아님"


# 중복 이름도 모두 저장하는지 확인
def test_duplicate_names(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n"
        "김철수,80\n"
        "김철수,90\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [("김철수", 80), ("김철수", 90)]
    assert skipped == []


# 빈 줄 무시 테스트
def test_blank_line(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n"
        "\n"
        "김철수,85\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [("김철수", 85)]
    assert skipped == []


# 존재하지 않는 파일 테스트
def test_missing_file(tmp_path):
    file = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_scores(file)


# 잘못된 줄의 번호 확인
def test_line_numbers(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n"
        "김철수,80\n"
        "이영희,abc\n"
        "박민수,101\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [("김철수", 80)]
    assert skipped[0][0] == 3
    assert skipped[1][0] == 4
