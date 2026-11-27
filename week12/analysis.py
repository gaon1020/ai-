import pandas as pd


# 데이터 정제
def 정제(df):
    df = df.copy()
    print("정제 전 행 수:", len(df))

    # 1. 점수가 비어 있는 행 삭제
    df = df.dropna(subset=["점수"])
    print("1단계 후 행 수:", len(df))

    # 2. 중복 행 삭제
    df = df.drop_duplicates()
    print("2단계 후 행 수:", len(df))

    # 3. 반과 과목의 앞뒤 공백 제거
    #df["반"] = df["반"].str.strip()
    #df["과목"] = df["과목"].str.strip()
    print("3단계 후 행 수:", len(df))

    # 4. 범위를 벗어나거나 정수가 아닌 점수 삭제
    df["점수"] = pd.to_numeric(df["점수"], errors="coerce")
    df = df[df["점수"].between(0, 100) & (df["점수"] % 1 == 0)]
    df["점수"] = df["점수"].astype(int)
    print("4단계 후 행 수:", len(df))

    return df


# 반별 평균 계산
def 반별평균(df):
    return df.groupby("반")["점수"].mean()


if __name__ == "__main__":
    df = pd.read_csv("scores_2026.csv", encoding="utf-8-sig")
    # 원본 데이터 확인
    print("전체 행과 열:", df.shape)
    print("빈 칸:", df["점수"].isna().sum())
    print("중복:", df.duplicated().sum())
    print("반 종류:", df["반"].unique())
    print("과목 종류:", df["과목"].unique())
    print(df["점수"].describe())

    # 데이터 정제
    df = 정제(df)

    print("정제 후 반 종류:", sorted(df["반"].unique()))
    print("정제 후 과목 종류:", sorted(df["과목"].unique()))

    # 1. 필터링
    math_scores = df[df["과목"] == "수학"]
    print("\n수학 행 수:", len(math_scores))

    # 2. 그룹화
    class_mean = 반별평균(df)
    print("\n반별 평균 점수")
    print(class_mean)

    subject_mean = df.groupby(["과목", "반"])["점수"].mean()
    print("\n과목별, 반별 평균 점수")
    print(subject_mean)

    # 3. 통계
    stats = df.groupby("반")["점수"].agg(
        ["count", "mean", "median", "max"]
    ).round(2)

    print("\n반별 통계")
    print(stats)

    # 과목별, 반별 개수 확인
    print("\n과목별, 반별 개수")
    print(df.groupby(["과목", "반"])["점수"].count())

    # 합계 검증
    print("\n반별 점수 합계:", df.groupby("반")["점수"].sum().sum())
    print("전체 점수 합계:", df["점수"].sum())

    # 개수 검증
    print("반별 개수 합계:", df.groupby("반")["점수"].count().sum())
    print("전체 행 수:", len(df))

    # 스팟 체크
    check = df[(df["반"] == "1반") & (df["과목"] == "수학")]["점수"]
    print("\n1반 수학 점수")
    print(check)
    print("점수 개수:", len(check))
    print("점수 합계:", check.sum())
    print("평균:", check.mean())

    # mini.csv 손계산 검증
    print("\nmini.csv 정제 결과")
    mini = pd.read_csv("mini.csv", encoding="utf-8-sig")
    mini = 정제(mini)

    print("정제 후 행 수:", len(mini))
    print("반별 평균")
    print(반별평균(mini))