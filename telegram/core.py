from math import ceil


class Paginator:
    def __init__(self, model, limit, page, query):
        self.limit = limit
        self.model = model
        self.query = query
        self.p = page
        self.count = 0

    def page(self):
        self.count = self.model.objects.raw("SELECT Count(*) as id " + self.query[self.query.find("FROM"):])[0].id
        return self.model.objects.raw(self.query + f" LIMIT {self.limit} OFFSET {(self.p - 1) * self.limit}")

    def number(self):
        return self.p

    def has_next(self):
        return self.p < ceil(self.count / self.limit)

    def next_page_number(self):
        return str(self.p + 1)

    def has_previous(self):
        return self.p > 1

    def previous_page_number(self):
        return str(self.p - 1)

    def page_range(self):
        return range(1, ceil(self.count / self.limit) + 1)
