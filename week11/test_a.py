
import pytest
from week11.load_scores import load_scores


# 정상 입력 테스트
def test_normal(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n"
        "김철수,85\n"
        "이영희,90\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [("김철수", 85), ("이영희", 90)]
    assert skipped == []


# 경계값 테스트 (0점, 100점)
def test_boundary(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n"
        "김철수,0\n"
        "이영희,100\n"
        "박민수,-1\n"
        "최지우,101\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [("김철수", 0), ("이영희", 100)]
    assert len(skipped) == 2
    assert skipped[0][2] == "점수가 0~100 밖"
    assert skipped[1][2] == "점수가 0~100 밖"


# 잘못된 점수 테스트
def test_invalid_score(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n"
        "김철수,abc\n"
        "이영희,\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == []
    assert skipped[0][2] == "점수가 정수가 아님"
    assert skipped[1][2] == "점수가 비어 있음"


# 이름이 비어 있는 경우
def test_empty_name(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n"
        ",80\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == []
    assert skipped == [(2, ",80", "이름이 비어 있음")]


# 열 개수가 잘못된 경우
def test_wrong_columns(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n"
        "김철수,80,추가\n"
        "이영희\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == []
    assert len(skipped) == 2
    assert all(s[2] == "열 개수가 2가 아님" for s in skipped)


# 빈 줄은 건너뛰고 기록하지 않는지 확인
def test_empty_line(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n"
        "\n"
        "김철수,80\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [("김철수", 80)]
    assert skipped == []


# 이름과 점수 앞뒤 공백 처리
def test_whitespace(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n"
        " 김철수 , 85 \n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [("김철수", 85)]
    assert skipped == []


# 파일이 존재하지 않는 경우
def test_file_not_found(tmp_path):
    file = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_scores(file)


# UTF-8 BOM 처리
def test_utf8_bom(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n김철수,90\n",
        encoding="utf-8-sig"
    )

    kept, skipped = load_scores(file)

    assert kept == [("김철수", 90)]
    assert skipped == []
