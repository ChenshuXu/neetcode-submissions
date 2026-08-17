class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        """
        This problem is equivalent to finding if a cycle exists in a directed graph. If a cycle exists, no topological ordering exists and therefore it will be impossible to take all courses.
        Topological sort with BFS.
        
        for each prerequisite:
        early course -> list of late course
        late course -> parent count+=1
        
        Topological sort with BFS.
        start with parent count==0
        
        Time and space complexity: O(E+V) where V is the number of courses, and E is the number of dependencies
        """
        # early course -> list of late course
        graph = {}
        # late course -> parent count+=1
        parentCount = {}
        for lateCourse, earlyCourse in prerequisites:
            if earlyCourse not in graph:
                graph[earlyCourse] = set()
            graph[earlyCourse].add(lateCourse)

            if lateCourse not in parentCount:
                parentCount[lateCourse] = 0
            parentCount[lateCourse] += 1
        
        
        allCourse = set()
        queue = collections.deque()
        for c in range(numCourses):
            allCourse.add(c)
            # find head (parent count==0)
            if c not in parentCount:
                parentCount[c] = 0
                queue.append(c)
        
        # Topological sort with BFS
        while queue:
            earlyCourse = queue.popleft()
            allCourse.remove(earlyCourse)
            if earlyCourse in graph:
                for lateCourse in graph[earlyCourse]:
                    parentCount[lateCourse] -= 1
                    # all prerequisite of lateCourse is taken
                    if parentCount[lateCourse] == 0:
                        queue.append(lateCourse)
        
        return len(allCourse) == 0