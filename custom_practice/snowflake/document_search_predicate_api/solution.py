from typing import List, Mapping, Optional


# A predicate is either None (match every document) or a tuple whose first
# element names the operator:
#   ("eq", field, value)        the whole field value equals value
#   ("contains", field, token)  the field has token as one of its words
#   ("and", *children)          every child matches; ("and",) matches everything
#   ("or", *children)           some child matches; ("or",) matches nothing
#   ("not", child)              the child does not match
Predicate = Optional[tuple]

# Returned for a leaf whose posting list does not exist. It is shared and never
# mutated, so no caller may treat a posting set as its own working set.
EMPTY_POSTINGS = frozenset()


class DocumentStore:
    """Store documents of named text fields and answer boolean field predicates."""

    def __init__(self) -> None:
        # Ids are handed out in insertion order, so sorting matched ids is the
        # required output order and no separate ordering pass is needed.
        self.doc_id_of = {}
        self.filename_of = {}
        self.next_doc_id = 0

        # doc_id -> the fields currently stored for it. Kept so an overwrite or
        # a delete can retract exactly the postings this document contributed.
        self.fields_of = {}

        # Inverted indexes, so a predicate leaf is one dict lookup instead of a
        # scan over every document.
        self.value_index = {}  # (field, whole value) -> set of doc ids
        self.token_index = {}  # (field, token) -> set of doc ids

        # The universe NOT is taken against: currently live documents only.
        self.live_ids = set()

    def insert_doc(self, filename: str, fields: Mapping[str, str]) -> None:
        """Insert or replace one document, keeping its original insertion position."""
        if filename in self.doc_id_of:
            # A replace reuses the id, so the document keeps its place in the
            # result order. Its old postings must go first, otherwise it keeps
            # matching words it no longer contains.
            doc_id = self.doc_id_of[filename]
            self._remove_postings(doc_id)
        else:
            doc_id = self.next_doc_id
            self.next_doc_id += 1
            self.doc_id_of[filename] = doc_id
            self.filename_of[doc_id] = filename

        # Copy the mapping so a later caller-side mutation cannot desynchronize
        # the stored fields from the index built out of them.
        stored_fields = dict(fields)
        self.fields_of[doc_id] = stored_fields
        self.live_ids.add(doc_id)
        self._add_postings(doc_id, stored_fields)

    def delete_doc(self, filename: str) -> bool:
        """Remove one document and report whether it was present."""
        if filename not in self.doc_id_of:
            return False

        doc_id = self.doc_id_of[filename]
        self._remove_postings(doc_id)
        del self.fields_of[doc_id]
        del self.doc_id_of[filename]
        del self.filename_of[doc_id]
        self.live_ids.discard(doc_id)
        # The id is retired rather than reused, so a later document with the
        # same filename sorts after everything already inserted.
        return True

    def search(self, predicate: Predicate = None) -> List[str]:
        """Return the filenames matching the predicate, in insertion order."""
        matched_ids = self._evaluate(predicate)
        results = []

        for doc_id in sorted(matched_ids):
            results.append(self.filename_of[doc_id])

        return results

    def _add_postings(self, doc_id: int, fields: Mapping[str, str]) -> None:
        """Index one document under its whole field values and its field words."""
        for field, value in fields.items():
            self.value_index.setdefault((field, value), set()).add(doc_id)
            # A repeated word adds the same id to the same set, so multiplicity
            # inside one field never duplicates a document in a result.
            for token in value.split():
                self.token_index.setdefault((field, token), set()).add(doc_id)

    def _remove_postings(self, doc_id: int) -> None:
        """Retract every posting the document's current fields produced."""
        for field, value in self.fields_of[doc_id].items():
            self._discard_posting(self.value_index, (field, value), doc_id)
            for token in value.split():
                self._discard_posting(self.token_index, (field, token), doc_id)

    @staticmethod
    def _discard_posting(index: dict, key: tuple, doc_id: int) -> None:
        postings = index.get(key)
        if postings is None:
            return

        postings.discard(doc_id)
        # Drop empty posting lists so the index stays proportional to live
        # content rather than to everything ever inserted.
        if not postings:
            del index[key]

    def _evaluate(self, predicate: Predicate) -> set:
        """Resolve one predicate node into the set of doc ids it matches."""
        # An empty predicate selects the whole live corpus.
        if predicate is None:
            return set(self.live_ids)

        operator = predicate[0]

        if operator == "eq":
            _, field, value = predicate
            # A missing field simply has no posting list, so it matches nothing.
            return set(self.value_index.get((field, value), ()))

        if operator == "contains":
            _, field, token = predicate
            return set(self.token_index.get((field, token), ()))

        if operator == "and":
            children = list(predicate[1:])
            # An AND with no conditions constrains nothing.
            if not children:
                return set(self.live_ids)

            # Start from the smallest posting list: every later intersection is
            # bounded by the set built so far, so the selective term does the
            # work instead of the common one.
            children.sort(key=self._estimated_size)
            # Only the smallest child is copied, because it becomes the working
            # set. Every later child is intersected against its stored posting
            # list directly, so a common term costs
            # min(len(working set), len(its postings)) instead of a full copy.
            matched = self._evaluate(children[0])

            for child in children[1:]:
                if not matched:
                    break
                matched = matched & self._postings(child)

            return matched

        if operator == "or":
            matched = set()
            for child in predicate[1:]:
                matched |= self._evaluate(child)
            return matched

        if operator == "not":
            _, child = predicate
            # NOT is only defined against the live universe. Complementing
            # against anything wider would resurrect deleted documents.
            return self.live_ids - self._evaluate(child)

        raise ValueError(f"unknown predicate operator: {operator!r}")

    def _postings(self, predicate: Predicate) -> frozenset:
        """Return a leaf's stored posting set without copying it."""
        if predicate is not None:
            operator = predicate[0]
            if operator == "eq":
                return self.value_index.get((predicate[1], predicate[2]), EMPTY_POSTINGS)
            if operator == "contains":
                return self.token_index.get((predicate[1], predicate[2]), EMPTY_POSTINGS)

        # A compound child has no stored posting list, so it has to be built.
        return self._evaluate(predicate)

    def _estimated_size(self, predicate: Predicate) -> int:
        """Estimate a child's match count so AND can intersect the smallest first."""
        if predicate is None:
            return len(self.live_ids)

        operator = predicate[0]

        if operator == "eq":
            return len(self.value_index.get((predicate[1], predicate[2]), ()))

        if operator == "contains":
            return len(self.token_index.get((predicate[1], predicate[2]), ()))

        # A compound child has no cheap estimate, so evaluate it last and let
        # the leaves narrow the candidate set first.
        return len(self.live_ids) + 1
