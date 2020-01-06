import csv
import time
import math

flows = set()
headers = ['PPS', 'FER', 'APPF', 'SFP', 'PS', 'H', 'dIP', 'sIP', 'lable1', 'lable2']
res = []  # 暂存十秒内的流表项
temp = []  #
flows_num = 0

data = open('/home/silentsamsara/桌面/SDNWORK/attack.csv', newline='')  # 数据集
result = open('/home/silentsamsara/桌面/SDNWORK/attack_data.csv', 'w', newline='')  # 特征向量保存文件

# data = open('C:/SDN/attack.csv')#数据集
# result = open('attack_data.csv', 'w', newline='')#特征向量保存文件


data_csv = csv.reader(data)
result_csv = csv.writer(result)
result_csv.writerow(headers)


def cal_PPS(flow_set):
    # 数据包速率
    length = len(flow_set)
    PPS = float(length / 2)
    return PPS


def cal_FER(flow_set, fnum):
    # 流表项生成率
    for i in flow_set:
        flows.update({i[3], i[4]})
    length = len(flows)
    new_num = length - fnum  # 新增流表项数目
    FER = float(new_num / 2)
    fnum = length  # 总流表项数据数目
    return FER, fnum, new_num  # FER 流表项数目 新增数目


def cal_APPF(flow_set):
    # 流表项的平均数据包数目
    temp_flows = set()
    for i in flow_set:
        temp_flows.update({i[3], i[4]})
    num = len(flows)
    APPF = len(flow_set) / num
    return APPF


def cal_SFP(flow_set):
    # 单流表项的数目

    temp_flows = set()
    setL = set()
    setR = set()
    for i in flow_set:
        temp = {(i[3], i[4])}
        temp_flows.update(temp)
    #        print(temp_flows)
    num = len(temp_flows)
    for i in temp_flows:
        #        print(i)
        setL.add(i[0])
        setR.add(i[1])
    setR = setL - setR
    single_num = len(setR)
    SEP = (float(single_num) / float(num))
    return SEP


def cal_PS(flow_set):
    k = 0
    type = ["eth:ethertype:ip:tcp", "eth:ethertype:ip:udp"]
    pro = [0.0, 0.0]
    for i in flow_set:
        for j in type:
            if i[2][0:20] == j:
                pro[k] = pro[k] + 1
                break
            k = k + 1
        k = 0
    M = len(flow_set)
    if pro[0] != 0 and pro[1] != 0:
        PS = -(((pro[0] / M) * math.log(pro[0] / M)) + ((pro[1] / M) * math.log(pro[1] / M)))
        return PS
    if pro[0] == 0 and pro[1] != 0:
        PS = -(pro[1] / M) * math.log(pro[1] / M)
        return PS
    if pro[0] != 0 and pro[1] == 0:
        PS = -(pro[0] / M) * math.log(pro[0] / M)
        return PS
    else:
        return 0


def cal_h_sIP_dIP(flow_set):
    print("cal_h_sIP_dIP")
    h = 0
    sIP = 0
    dIP = 0
    temp_flows = set()
    srcIP = set()
    dstIP = set()
    dstPort = set()

    for i in flow_set:
        #   print(i)
        temp = {(i[3], i[4], i[6])}
        temp_flows.update(temp)
    for i in temp_flows:
        srcIP.add(i[0])
        dstIP.add(i[1])
        dstPort.add(i[2])
    srcList = list(srcIP)
    dstList = list(dstIP)
    PortList = list(dstPort)
    # 计算H(srcIP|dstIP)
    A = [[] for i in range(len(dstList))]
    B = [[[] for i in range(len(dstList))] for i in range(len(srcList))]
    # Init
    for i in range(len(dstList)):
        A[i] = 0
    for i in range(len(srcList)):
        for j in range(len(dstList)):
            B[i][j] = 0
    # print(srcList)
    #  print(dstList)
    flag = 0
    for k in flow_set:  # 每一个数据包
        for i in range(len(srcList)):
            for j in range(len(dstList)):
                # print(k[3],k[4])
                if srcList[i] == k[3] and dstList[j] == k[4]:
                    B[i][j] += 1
                    A[j] += 1
                    flag = 1
                    break
            if flag == 1:
                flag = 0
                break
    for j in range(len(dstList)):
        tempj = (float(A[j]) / float(len(flow_set)))
        tempi = 0
        for i in range(len(srcList)):
            if B[i][j] != 0 and A[j] != 0:
                tempi += ((float(B[i][j]) / float(A[j]))) * (math.log(float(B[i][j]) / float(A[j])))
        h += tempj * tempi
    h = -h

    # 计算H(dstPort|dstIP)
    C = [[[] for i in range(len(dstList))] for i in range(len(PortList))]
    # Init
    for i in range(len(PortList)):
        for j in range(len(dstList)):
            C[i][j] = 0

    for k in flow_set:  # 每一个数据包
        for i in range(len(PortList)):
            for j in range(len(dstList)):
                if PortList[i] == k[6] and dstList[j] == k[4]:
                    C[i][j] += 1
    for j in range(len(dstList)):
        tempj = (float(A[j]) / float(len(flow_set)))
        tempi = 0
        for i in range(len(PortList)):
            if C[i][j] != 0 and A[j] != 0:
                tempi += (float(C[i][j]) / float(A[j])) * (math.log(float(C[i][j]) / float(A[j])))
        dIP += tempj * tempi
    dIP = -dIP

    # 计算H(srcIP|dstPort)
    D = [[] for i in range(len(PortList))]
    E = [[[] for i in range(len(PortList))] for i in range(len(srcList))]
    # Init
    for i in range(len(PortList)):
        D[i] = 0
    for i in range(len(srcList)):
        for j in range(len(PortList)):
            E[i][j] = 0
    for k in flow_set:  # 每一个数据包
        for i in range(len(srcList)):
            for j in range(len(PortList)):
                if srcList[i] == k[3] and PortList[j] == k[6]:
                    E[i][j] += 1
                    D[j] += 1
    for j in range(len(PortList)):
        tempj = float(D[j]) / float(len(flow_set))
        tempi = 0
        for i in range(len(srcList)):
            if E[i][j] != 0 and D[j] != 0:
                tempi += (float(E[i][j]) / float(D[j])) * (math.log(float(E[i][j]) / float(D[j])))
        sIP += tempj * tempi
    sIP = -sIP

    return h, sIP, dIP


cnt = 0
Time = -1
sec_cnt = 0

for row in data_csv:
    if len(row) == 1:
        continue
    timestamp = row[1]
    timestamp = float(timestamp)

    localtime = time.localtime(timestamp)
    timestamp = localtime.tm_sec
    #    print(timestamp)

    if Time == -1:
        Time = timestamp

    res.append(row)  # res保存了十秒内的流表项
    #    print(res)
    if timestamp - Time == 1 or timestamp - Time == -59:
        print(len(res))
        if len(res) > 10000:
            Time = -1
            res = []
            temp = []
            continue
        pps = cal_PPS(res)
        fer, flows_num, new_flows_num = cal_FER(res, flows_num)
        appf = cal_APPF(res)
        sfp = cal_SFP(res)

        ps = cal_PS(res)
        h, sIP, dIP = cal_h_sIP_dIP(res)

        temp.append(pps)
        temp.append(fer)
        temp.append(appf)
        temp.append(sfp)
        temp.append(ps)
        temp.append(h)
        temp.append(sIP)
        temp.append(dIP)
        temp.append(0)
        temp.append(0)
        result_csv.writerow(temp)

        cnt += 1
        # if cnt > 20:
        #     break
        print("------CNT------", cnt)
        sec_cnt = 0
        Time = -1
        res = []
        temp = []
    #    temp_flows = [] #流表项 集合
