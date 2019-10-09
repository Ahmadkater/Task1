from firebase import firebase
import functions as f
import json
import time

fire = firebase.FirebaseApplication('https://proj1-6f30a.firebaseio.com/',None)

data = fire.get("/macs", None)

print(data)

diction = dict()
diction["macs"] = data


def algorithm(point):

    t_point = f.cal_avg_std(point)

    ref_points = json.loads(open("all-points.json").read())

    for p in ref_points:
        p["marker"] = -1

    flag = f.find_flag(t_point)

    pre_matched_points = f.get_matched_points(ref_points,flag)

    for p in pre_matched_points:
        print(p)

    points = f.improved_euclidean_dis(t_point, pre_matched_points)

    least_closest_points = f.sort_by_euclidean_dis(points)

    print("**least_closest_points**")
    for p in least_closest_points:
        print(p)

    co_ordinates1 = f.get_position_acc_to_closest_points(least_closest_points)

    print("**x1,y1 **")
    for co_ord in co_ordinates1:
        print(co_ord)

    reverse = []
    reverse.append(co_ordinates1[1])
    reverse.append(co_ordinates1[0])

    fire.put("/","result",reverse)


algorithm(diction)

while True:

    if(fire.get("/flag",None)):

        real_data = data
        data = fire.get("/macs", None)
        diction["macs"] = data
        print(diction)
        if real_data != data:
            algorithm(diction)
        fire.put("/","flag",False)
