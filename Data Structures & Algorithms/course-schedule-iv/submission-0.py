class Solution:
    def checkIfPrerequisite(
        self,
        numCourses: int,
        prerequisites: List[List[int]],
        queries: List[List[int]]
    ) -> List[bool]:
        # earlyCourse -> lateCourses
        graph = collections.defaultdict(list)
        indegree = collections.defaultdict(int)

        for earlyCourse, lateCourse in prerequisites:
            graph[earlyCourse].append(lateCourse)
            indegree[lateCourse] += 1

        queue = collections.deque()

        for course in range(numCourses):
            if indegree[course] == 0:
                queue.append(course)

        # course -> all direct and indirect prerequisites
        prerequisiteMap = collections.defaultdict(set)

        while queue:
            earlyCourse = queue.popleft()

            for lateCourse in graph[earlyCourse]:
                # Direct prerequisite
                prerequisiteMap[lateCourse].add(earlyCourse)

                # Indirect prerequisites
                prerequisiteMap[lateCourse].update(
                    prerequisiteMap[earlyCourse]
                )

                indegree[lateCourse] -= 1

                if indegree[lateCourse] == 0:
                    queue.append(lateCourse)

        result = []

        for earlyCourse, lateCourse in queries:
            result.append(
                earlyCourse in prerequisiteMap[lateCourse]
            )

        return result