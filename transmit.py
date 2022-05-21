import re


class SearchOptions:
    def set(self, budget, category, next_day_delivery, prefec_code):

        budget = budget.replace("1万", "10000")
        if "~" in budget:
            budget = budget.split("~")
            self.minPrice = int(re.sub(r"\D", "", budget[0]))
            self.maxPrice = int(re.sub(r"\D", "", budget[1]))
        else:  # "1万円以上"の選択肢には上限がない
            self.minPrice = 10000
            self.maxPrice = 99999999

        if category == "レディースファッション":
            self.genreId = 100371
        elif category == "メンズファッション":
            self.genreId = 551177
        elif category == "日用品雑貨・文房具・手芸":
            self.genreId = 215783

        if next_day_delivery == '希望':
            self.asurakuFlag = True
            self.asurakuArea = prefec_code
        elif next_day_delivery == '指定なし':
            self.asurakuFlag = False
            self.asurakuArea = 0
