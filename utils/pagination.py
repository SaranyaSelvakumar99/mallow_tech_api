def pagination_handler(total_count, page, limit):
    if page == 1:
        offset = 0
    else:
        offset = (page - 1) * limit
    
    count_1 = total_count % limit
    count_2 = total_count // limit
    if count_1 != 0:
        count_2 += 1

    return offset, limit, total_count, count_2
