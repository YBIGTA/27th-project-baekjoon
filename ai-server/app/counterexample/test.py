import asyncio
import logging
from app.counterexample.runner import runner

PROBLEM="""
# 2×n 타일링 2

|시간 제한|     메모리 제한     |제출   |정답   |맞힌 사람      |정답 비율|
|-------|----------|------|------|---------|------|
|1 초   |256 MB    |93159 |54898 |44518    |58.331%|
## 문제
2×n 직사각형을 1×2, 2×1과 2×2 타일로 채우는 방법의 수를 구하는 프로그램을 작성하시오.

아래 그림은 2×17 직사각형을 채운 한가지 예이다.



## 입력
첫째 줄에 n이 주어진다. (1 ≤ n ≤ 1,000)

## 출력
첫째 줄에 2×n 크기의 직사각형을 채우는 방법의 수를 10,007로 나눈 나머지를 출력한다.

### 예제 입력 1 
2
### 예제 출력 1 
3
### 예제 입력 2 
8
### 예제 출력 2 
171
### 예제 입력 3 
12
### 예제 출력 3 
2731
"""

USERCODE="""
MOD = 100007
N = int(input())

if N <= 2:
    print([1, 3][N - 1])
else:
    a, b = 1, 3
    for _ in range(N - 2):
        a, b = b, (b + 2 * a) % MOD
    print(b)
"""
async def run_counterexample():
    result = await runner.find_counterexample(
        problem_description=PROBLEM, 
        language="python", 
        user_code=USERCODE,
        difficulty=8
    )
    print(result)
    return result

# set logging level to INFO
logging.basicConfig(level=logging.INFO)

# run counterexample
asyncio.run(run_counterexample())
