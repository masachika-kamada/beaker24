import re


class SearchOptions:
    def set(self, budget, category, next_day_delivery, prefec_code, wrapping):

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

        if next_day_delivery == "希望する":
            self.asurakuFlag = 1
            self.asurakuArea = prefec_code
        elif next_day_delivery == "指定なし":
            self.asurakuFlag = 0
            self.asurakuArea = 0

        if wrapping == "希望する":
            self.giftFlag = 1
        elif wrapping == "指定なし":
            self.giftFlag = 0


class SearchResult:
    def __init__(self, item_name, item_url, image_url, review, n_review,
                 asuraku_flag, asuraku_area):
        self.itemName = item_name
        self.itemUrl = item_url
        self.imageUrl = image_url
        self.review = review
        self.n_review = n_review
        if asuraku_flag == 1:
            self.nextDayDelivery = "可"
            self.asurakuArea = asuraku_area
        else:
            self.nextDayDelivery = "不可"
