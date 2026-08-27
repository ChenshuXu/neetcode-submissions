import collections
from functools import cache
from itertools import combinations
from typing import List


RunningState = tuple[tuple[int, int], ...]
CompletedState = frozenset[int]


class Solution:
    def minimumTime(
        self,
        n: int,
        relations: List[List[int]],
        time: List[int],
        workerCount: int,
    ) -> int:
        # earlyCourse -> list of lateCourse
        graph = collections.defaultdict(list)

        # lateCourse -> number of unfinished early courses
        parentCount = collections.defaultdict(int)

        # lateCourse -> set of all direct prerequisite courses
        parentCourses = collections.defaultdict(set)

        for earlyCourse, lateCourse in relations:
            graph[earlyCourse].append(lateCourse)
            parentCount[lateCourse] += 1
            parentCourses[lateCourse].add(earlyCourse)

        queue = collections.deque()
        for course in range(1, n + 1):
            if parentCount[course] == 0:
                queue.append(course)

        # Keep the same Kahn traversal as Parallel Courses III.
        topologicalOrder = []
        while queue:
            earlyCourse = queue.popleft()
            topologicalOrder.append(earlyCourse)

            for lateCourse in graph[earlyCourse]:
                parentCount[lateCourse] -= 1
                if parentCount[lateCourse] == 0:
                    queue.append(lateCourse)

        totalDuration = sum(time)

        @cache
        def solve(
            completedCourses: CompletedState,
            runningCourses: RunningState,
        ) -> int:
            if len(completedCourses) == n:
                return 0

            runningCourseSet = set()
            for course, _ in runningCourses:
                runningCourseSet.add(course)

            readyCourses = []
            for course in topologicalOrder:
                if course in completedCourses:
                    continue
                if course in runningCourseSet:
                    continue

                parents = parentCourses[course]
                if parents.issubset(completedCourses):
                    readyCourses.append(course)

            freeWorkerCount = workerCount - len(runningCourses)
            startCount = min(freeWorkerCount, len(readyCourses))
            bestRemainingTime = totalDuration + 1

            # Unlike LC2050, ready courses compete for limited workers.
            # Try every possible priority choice to preserve global optimality.
            for coursesToStart in combinations(readyCourses, startCount):
                nextRunningCourses = list(runningCourses)
                for course in coursesToStart:
                    nextRunningCourses.append((course, time[course - 1]))

                timeUntilNextFinish = min(
                    remainingTime
                    for _, remainingTime in nextRunningCourses
                )

                nextCompletedCourses = set(completedCourses)
                stillRunning = []

                for course, remainingTime in nextRunningCourses:
                    remainingTime -= timeUntilNextFinish

                    if remainingTime == 0:
                        nextCompletedCourses.add(course)
                    else:
                        stillRunning.append((course, remainingTime))

                stillRunning.sort()
                candidateTime = timeUntilNextFinish + solve(
                    frozenset(nextCompletedCourses),
                    tuple(stillRunning),
                )
                bestRemainingTime = min(bestRemainingTime, candidateTime)

            return bestRemainingTime

        return solve(frozenset(), ())
