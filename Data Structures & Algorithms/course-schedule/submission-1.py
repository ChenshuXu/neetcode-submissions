class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # For each pair [lateCourse, earlyCourse], 
        # I’ll add an edge from the early course to the late course. 
        # Then I’ll use three-state DFS to detect a cycle. 
        # If I reach a course that is already on the current DFS path, 
        # I’ve found a cycle. If a course is already marked as done, 
        # all outgoing paths from that course were previously verified as cycle-free.
        
        # earlyCourse -> courses unlocked after earlyCourse
        graph = collections.defaultdict(list)
        for lateCourse, earlyCourse in prerequisites:
            graph[earlyCourse].append(lateCourse)

        UNVISITED = 0  # white: never checked
        VISITING = 1   # gray: on the current DFS path
        DONE = 2       # black: this dependency path is cycle-free
        state = [UNVISITED] * numCourses

        def dfs(earlyCourse):
            # Meet a gray course again: the current path contains a cycle.
            if state[earlyCourse] == VISITING:
                return False

            # Meet a black course: its outgoing paths were already checked.
            if state[earlyCourse] == DONE:
                return True

            # Enter this course: turn it gray.
            state[earlyCourse] = VISITING

            for lateCourse in graph[earlyCourse]:
                if not dfs(lateCourse):
                    return False

            # Every outgoing dependency path is safe: turn it black.
            state[earlyCourse] = DONE
            return True

        for course in range(numCourses):
            if not dfs(course):
                return False

        return True