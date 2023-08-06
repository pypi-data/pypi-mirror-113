# This file contains the clashgap implementation
# and all the functions required for the clashgap function

def _list_has(arr, index):
    return (len(arr) > index)

def _max_elem(arr):
    arb_val = len(arr[0])
    index = 0
    for i in range(len(arr)):
        if len(arr[i]) > arb_val:
            arb_val = len(arr[i])
            index = i
    return arr[index]

def gap(clash):
    res = []
    buff = ['', '']
    for i in range(len(_max_elem(clash))):
        if _list_has(clash[0], i):
            buff[0] += clash[0][i]
        if _list_has(clash[1], i):
            buff[1] += clash[1][i]

        collision = -1
        k = 0
        for j in range(len(buff[0])):
            collision = buff[1].find(buff[0][j])
            if not(collision == -1):
                k = j
                break
        else:
            continue
            
        if not(collision == -1):
            if buff[0][:j] or buff[1][:collision]:
                res += [[buff[0][:j], buff[1][:collision]], buff[1][collision]]
            else:
                if len(res) == 0:
                    res += buff[1][collision]
                elif type(res[-1]) is list:
                    res += buff[1][collision]
                else:
                    res[-1] += buff[1][collision]
            
            buff[0] = buff[0][j+1:]
            buff[1] = buff[1][collision+1:]
    if buff[0] or buff[1]:
        res.append(buff)

    return res

