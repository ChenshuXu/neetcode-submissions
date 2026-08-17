class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        # early course -> list of late course
        graph = {}
        # late course -> number of early course
        parentCount = {}

        for lateCourse, earlyCourse in prerequisites:
            if lateCourse not in parentCount:
                parentCount[lateCourse] = 0
            parentCount[lateCourse] += 1

            if earlyCourse not in graph:
                graph[earlyCourse] = set()
            graph[earlyCourse].add(lateCourse)
        
        # topolicical sort with bfs
        result = []
        allCourse = set()
        queue = collections.deque()
        for c in range(numCourses):
            allCourse.add(c)
            if c not in parentCount:
                parentCount[c] = 0
                queue.append(c)
        
        while queue:
            earlyCourse = queue.popleft()
            allCourse.remove(earlyCourse)
            result.append(earlyCourse)
            if earlyCourse in graph:
                for lateCourse in graph[earlyCourse]:
                    parentCount[lateCourse] -= 1
                    if parentCount[lateCourse] == 0:
                        queue.append(lateCourse)
        
        if len(allCourse) == 0:
            return result
        return []