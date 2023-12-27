def get_num_of_last_page(length: int) -> int:
    if length % 10 > 0:
        return length // 10 + 1
    else:
        return length // 10
