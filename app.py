import os
from itertools import groupby
from flask import Flask
from flask import render_template, request

app = Flask(__name__)


@app.route("/")
def form():
    return render_template("form.html")


@app.route("/", methods=["POST"])
def my_form_post():
    euros = request.form["euros"]
    usd = round(2.25, 2)

    return render_template("form.html", euros=euros, usd=usd)


def get_raw_latest_activity_data():
    import csv

    users = """Id,	First,	last,	program	
1,	John,	Smith,	CRONs
2,	Dave,	lir,	CRONs
3,	James,	kan,	CRONs
4,	William,	Duglas,	CRONs
5,	John,	Lin,	CRONs
6,	Jeff,	Miller,	CRONs
7,	Dan,	Shultz,	CRONs""".replace('\t', '').splitlines()

    user_actions = """user ID,time,type,description
1,	2/22/21 13:11,	steps,	11000
1,	2/23/21 13:11,	medication,	Done
1,	2/22/21 13:11,	Mind,	Energy level
1,	2/22/21 13:05,	PRO,	15 - Mid
1,	2/23/21 13:05,	water,	2 cups
2,	2/24/21 13:05,	Mind,	Quality of sleep
3,	2/25/21 13:05,	medication,	done
4,	2/26/21 13:05,	PRO,	5 low
5,	2/27/21 13:05,PRO,	20 critical
""".replace('\t', '').splitlines()

    user_actions = list(csv.DictReader(user_actions))
    dict_u_actions = make_dict_with_lists(user_actions, lambda x: x['user ID'])
    users = {x['Id']: x for x in csv.DictReader(users)}

    return users, dict_u_actions


def make_dict_with_lists(iterable, key_func):
    dict_ret = {k: list(v) for k, v in groupby(sorted(iterable, key=key_func), key=key_func)}
    return dict_ret


def increasing(arr):
        return True


def create_aggregations(data):
    users = data[0]
    user_actions = data[1]

    users_all = dict()
    for user_id, actions in user_actions.items():
        dd = make_dict_with_lists(actions, key_func=lambda g: g['type'])
        max_by_type = {f'updates_for_{action_type}': lambda: sorted(lst_actions_by_type, key=lambda x: x['time'])
                       for action_type, lst_actions_by_type in dd.items()
                       }

        per_user_stats = {
            'last_update_date': lambda: max(actions, key=lambda g: g['time']),
            **max_by_type
        }
        per_user_stats.update({
            'PRO_increase': lambda: increasing(per_user_stats['updates_for_PRO'])
        })

        users_all[user_id] = per_user_stats


if __name__ == "__main__":
    import rule_engine
    from datetime import datetime

    data = get_raw_latest_activity_data()
    rule_readable_data = create_aggregations(data)

    # match a literal first name and applying a regex to the email
    rule = rule_engine.Rule(
        'PRO_increase == "True" and since =~ ".*@rebels.org$"'
    )  # => <Rule text='first_name == "Luke" and email =~ ".*@rebels.org$"' >
    rule.matches({
        'first_name': 'Luke', 'last_name': 'Skywalker', 'email': 'luke@rebels.org'
    })  # => True
    rule.matches({
        'first_name': 'Darth', 'last_name': 'Vader', 'email': 'dvader@empire.net'
    })  # => False

    is_dev = os.environ.get('USERNAME', 'root') != 'root'
    app.run(debug=is_dev, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
