import pandas as pd


df = pd.read_csv('user_journey_raw.csv')


# 1. Remove duplicates from the user_journey column

def remove_page_duplicates(datafr, target_column='user_journey'):
    new_journey_col = []
    for journey in datafr[target_column]:
        list_ = journey.split('-')
        no_duplicates = []
        for page in list_:
            if page not in no_duplicates:
                no_duplicates.append(page)
        new_journey_col.append(no_duplicates)

    # turn the list of lists (new_journey_col) into a series to be able to join the words back with '-'
    s = pd.Series(new_journey_col)
    new_journey = s.str.join('-')

    # create a copy of the original dataframe with an updated column
    data = datafr.copy(deep=True)
    data[target_column] = new_journey
    return data


data = remove_page_duplicates(df, 'user_journey')
# print(data.head())


# 2. Group user_journey(s) by user_id

def group_by(datafr, group_by_col='user_id', target_col='user_journey', sessions='all', count_from='last'):
    datafr[target_col] = datafr.groupby([group_by_col])[target_col].transform(lambda x: "-".join(x.str.strip()))
    data_cl = datafr.copy(deep=True)
    data_cl = data_cl.drop_duplicates(subset="user_id")
    return data_cl


clean_data = group_by(data)
# print(clean_data.head())


# 3. Remove all unnecessary pages (data scientist's choice)

def remove_pages(data, pages:list, target_col='user_journey'):
    kept_pages_col = []
    for list_ in data[target_col]:
        lst = list_.split('-')
        kept_pages = []
        for page in lst:
            if page not in pages:
                kept_pages.append(page)
            else:
                page +1
        kept_pages_col.append(kept_pages)

    # turn the list of lists (new_journey_col) into a series to be able to join the words back with '-'
    s = pd.Series(kept_pages_col)
    new_pages = s.str.join('-')

    # create a copy of the original dataframe with an updated column
    stripped_pages_data = data.copy(deep=True)
    stripped_pages_data[target_col] = new_pages
    return stripped_pages_data

# print(remove_pages(clean_data, ['Log in', 'Other'])) - getting some Nans here (need to sort out what happens if all pages a user clicked on are removed)
