from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np


def draw_charts(expenses):
    total_amount_by_category = {}
    for expense in expenses:
        expense_category = expense.category.name
        if expense_category not in total_amount_by_category.keys():
            total_amount_by_category[expense_category] = expense.spend
        else:
            total_amount_by_category[expense_category] += expense.spend
    sorted_amount_by_category = dict(sorted(total_amount_by_category.items(), key=lambda item: item[1], reverse=True))

    categories = sorted_amount_by_category.keys()
    values = [value for value in sorted_amount_by_category.values()]

    max_value_index = values.index(max(values))

    explode = [0 for x in values]
    explode[max_value_index] = 0.1
    fig, ax = plt.subplots()
    ax.pie(values, explode=explode, labels=categories,
           autopct='%1.1f%%', shadow=True)
    ax.axis('equal')

    fig.set_facecolor((1, 0.992, 0.91))
    fig.subplots_adjust(top=0.8, right=0.7)

    values = np.array(values)
    percents = 100. * values / values.sum()

    labels = ['{0} - {1:1.2f} %'.format(i, j) for i, j in zip(categories, percents)]

    legend = ax.legend(labels=labels, loc='upper right', bbox_to_anchor=(1.5, 1.1))
    fig.bbox_extra_artists = (legend,)

    image = BytesIO()
    fig.savefig(image)

    return image.getvalue()
