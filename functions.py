import statistics
import math
from operator import  itemgetter


# def cal_avg_std(p):
#     for i in range(len(p["macs"])):
#         avg = statistics.mean(p["macs"][i]["value"])
#         std = statistics.stdev(p["macs"][i]["value"], xbar=avg)
#         p['macs'][i]['value'] = {"avg": avg, "std": std}
#
#     return p

def cal_avg_std(p):

    for i in range(len(p["macs"])):

        if len(p["macs"][i]['value']) <= 1:
            p["macs"][i]['value'].append(-100)
            p["macs"][i]['value'].append(-100)

        avg = statistics.mean(p["macs"][i]["value"])
        std = statistics.stdev(p["macs"][i]["value"], xbar=avg)
        p['macs'][i]['value'] = {"avg": avg, "std": std}

    return p

def improved_euclidean_dis(test,finger_prints):
    d = 0
    d_arr = []
    for item in finger_prints:
        for i in range(len(item["macs"])):
            d_i = (abs(test['macs'][i]['value']['avg']-item['macs'][i]['value']['avg'])+test['macs'][i]['value']['std']+item['macs'][i]['value']['std'])**2
            d += d_i
        d_arr.append(math.sqrt(d))
        d = 0
    j=0
    print("euclidean distance array : ",d_arr)
    for item in finger_prints:
        item["d"] = d_arr[j]
        j=j+1

    return finger_prints


def sort_by_euclidean_dis(values):
    values = sorted(values, key=itemgetter('d'))

    return values[:3]

def sort_by_joint_prob(values):
    values = sorted(values, key=itemgetter('p'),reverse=True)

    return values[:3]

def find_flag(t):

    arr = []
    arr2 = []
    for router in t['macs']:
        arr.append(router["value"]["avg"])

    flag = statistics.mean(arr)

    for router in t['macs']:
        if router["value"]["avg"] > flag:
            arr2.append({"name":router["name"] , "avg":router["value"]["avg"]})

    return arr2


def pre_matching(flag,point):
    marker = len(flag)
    for i in range(len(point["macs"])):
        for j in range(len(flag)):
            if point["macs"][i]["name"]== flag[j]["name"]:
                if point["macs"][i]["value"]["avg"] >= flag[j]["avg"]:
                    marker = marker-1
                    point["marker"] = marker
    return point


def get_matched_points(points,flag1):
    arr = []
    for p in points:
        pre_matching(flag1,p)
        if p["marker"] <= 1 and p["marker"] != -1:
            arr.append(p)
    return arr

def get_position_acc_to_closest_points(values):

    sum_w = 0
    sum_wx = 0
    sum_wy = 0
    for item in values:
        sum_w += 1 / item["d"]
        sum_wx += (1 / item["d"]) * float(item["x"])
        sum_wy += (1 / item["d"]) * float(item["y"])

    return [sum_wx/sum_w,sum_wy/sum_w ]



def improved_joint_prop(test,finger_prints):
    pi =1
    p = []
    for item in finger_prints:
        for i in range(len(item["macs"])):
            if (item["macs"][i]['value']['std']) != 0 :
                b = 1 / (item['macs'][i]['value']['std'] * math.sqrt(2 * math.pi))
                c = ((test['macs'][i]['value']['avg'] - item['macs'][i]['value']['avg']) ** 2) / (
                        2 * ((item['macs'][i]['value']['std']) ** 2))
                pi = b * math.exp(c)
                # print("b = 1/segma*sqrt2*pi", b)
                # print("c = avgt - avgmean / 2*segma", c)
                # print(pi)
                pi *= pi

        p.append(pi)
    j = 0
    print("joint probability array : ", p)
    for item in finger_prints:
        item["p"] = p[j]
        j = j+1

    return finger_prints


def get_position_x2_y2(values):

    sum_w = 0
    sum_wx = 0
    sum_wy = 0
    for item in values:
        sum_w += math.log(item["p"])
        sum_wx += math.log(item["p"]) * float(item["x"])
        sum_wy += math.log(item["p"]) * float(item["y"])

    return [sum_wx/sum_w,sum_wy/sum_w ]

def get_x_y(shortest_ed , largest_jp,p1,p2):
    d_arr = []
    p_arr = []
    for item in shortest_ed:
        d_arr.append(item['d'])

    for item in largest_jp:
        p_arr.append(item['p'])

    d1 = statistics.variance(d_arr,xbar= statistics.mean(d_arr))
    d2 = statistics.variance(p_arr, xbar=statistics.mean(p_arr))

    print("d-arr" , d_arr , "v1" , d1)
    print("p-arr", p_arr, "v2", d2)

    x = p1[0] * (d1/(d1+d2)) + p2[0] * (d2/(d1+d2))

    y = p1[1] * (d1/(d1+d2)) + p2[1] * (d2/(d1+d2))

    return [x,y]



# p = []

# def improved_joint_prop(test,finger_prints):
#     pi =1
#     for item in finger_prints:
#         for i in range(len(item["macs"])):
#             b = 1/(item['macs'][i]['value']['std']*math.sqrt(2*math.pi))
#             c = ( (test['macs'][i]['value']['avg']-item['macs'][i]['value']['avg'])**2 ) /(2*((item['macs'][i]['value']['std'])**2))
#             pi = b * math.exp( c )
#             print("b = 1/segma*sqrt2*pi", b)
#             print("c = avgt - avgmean / 2*segma",c)
#             print(pi)
#             pi *=pi
#         p.append(pi)
#
# print("************************")
# print(p)
# print(improved_joint_prop(t,points))
