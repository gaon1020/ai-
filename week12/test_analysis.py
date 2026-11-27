import pandas as pd
from analysis import 정제, 반별평균

df = 정제(pd.read_csv("scores_2026.csv", encoding="utf-8-sig"))
mini = 정제(pd.read_csv("mini.csv", encoding="utf-8-sig"))


# 1. 정제 후 행 수 확인
def test_행수():
    assert len(df) == 100


# 2. 반 종류 확인
def test_반종류():
    assert sorted(df["반"].unique()) == ["1반", "2반"]


# 3. 그룹 합계와 전체 합계 비교
def test_합계():
    group_sum = df.groupby("반")["점수"].sum().sum()
    total_sum = df["점수"].sum()

    assert group_sum == total_sum
    assert df.groupby("반")["점수"].count().sum() == len(df)


# 4. 손계산 결과와 비교
def test_손계산():
    assert len(mini) == 7
    assert 반별평균(mini)["1반"] == 80.0
    assert 반별평균(mini)["2반"] == 70.0