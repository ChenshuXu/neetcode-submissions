from typing import Optional


class TimestampedVersionedKV:
    """Store timestamped key versions with TTL-aware point-in-time reads."""

    def __init__(self) -> None:
        """Initialize an empty store."""
        # key -> list of [write_time, value, expire_time], ordered by write time
        self.data = {}
        

    def set(self, key: str, value: str, write_time: int, ttl: int) -> None:
        """Add or replace one version identified by key and write_time."""
        if key not in self.data:
            self.data[key] = []
        version_list = self.data[key]

        if len(version_list) == 0:
            version_list.append([write_time, value, write_time + ttl])
            return

        # find the position should be, the version list is ordered by write time
        # binary search to find largest i, version_list[i].write_time <= write_time
        # if version_list[i].write_time == write_time, replace it, else, add new
        target_index = -1
        left = 0
        right = len(version_list) - 1
        while left <= right:
            mid = (left + right) // 2
            if version_list[mid][0] > write_time:
                right = mid - 1
            elif version_list[mid][0] == write_time:
                # replace it
                version_list[mid] = [write_time, value, write_time + ttl]
                return
            else:
                target_index = mid
                left = mid + 1

        # insert after target_index
        version_list.insert(target_index + 1, [write_time, value, write_time + ttl])


    def get(self, key: str, query_time: int) -> Optional[str]:
        """Return the visible unexpired value at query_time, or None."""
        if key not in self.data:
            return None

        version_list = self.data[key]
        # binary search to find the rightmost write_time <= query_time
        target_index = -1
        left = 0
        right = len(version_list) - 1

        while left <= right:
            mid = (left + right) // 2
            if version_list[mid][0] <= query_time:
                target_index = mid
                left = mid + 1
            else:
                right = mid - 1

        if target_index == -1:
            return None

        selected_version = version_list[target_index]
        value = selected_version[1]
        expire_time = selected_version[2]
        if query_time < expire_time:
            return value
        return None

    def snapshot(self, query_time: int) -> dict[str, str]:
        """Return all key-value pairs visible and unexpired at query_time."""
        result = {}
        for key in self.data:
            value = self.get(key, query_time)
            if value is not None:
                result[key] = value
        return result
