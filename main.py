import random
import copy
import timeit
import plotly.graph_objects as go
from plotly.subplots import make_subplots

## Algorithms:

def selection_sort(a):
    global c
    for i in range(len(a)):
        c += 1 #count
        min_idx = i
        for j in range(i+1, len(a)):
            c += 1 #count
            if a[min_idx] > a[j]:
                c += 1 #count
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]

def insertion_sort(arr):
    global c
    for i in range(1, len(arr)):
        c += 1 #count
        key = arr[i]
        j = i-1
        while j >= 0 and key < arr[j] :
                c += 1 #count
                arr[j + 1] = arr[j]
                j -= 1
        arr[j + 1] = key


def merge(f, s):
    md_list = []
    i, j = 0, 0
    global c
    while i != len(f) and j != len(s):
        c += 1 #count
        if f[i] < s[j]:
            c += 1 #count
            md_list.append(f[i])
            i += 1
        else:
            c += 1 #count
            md_list.append(s[j])
            j += 1
    md_list.extend(f[i:])
    md_list.extend(s[j:])
    return md_list

def merge_sort(a):
    b = []
    global c
    for i in range(len(a)):
        c += 1 #count
        b.append([a[i]])
    i = 0
    while i < len(b) - 1:
        c += 1 #count
        L1 = b[i]
        L2 = b[i + 1]
        newL = merge(L1, L2)
        b.append(newL)
        i += 2
    if len(b) != 0:
        c += 1 #count
        a[:] = b[-1][:]


def shell_sort(a):
    global c
    n = len(a)
    g = n // 2
    while g > 0:
        c += 1 #count
        for i in range(g, n):
            c += 1 #count
            temp = a[i]
            j = i
            while j >= g and a[j - g] > temp:
                c += 1 #count
                a[j] = a[j - g]
                j -= g
            a[j] = temp
        g //= 2


## Initialisation

def test_code(f,a):
    return '''{}({})'''.format(fname, a), '''from __main__ import {}'''.format(fname)

def exp_0(f, p):
    global c
    time = []
    fname = f.__name__ 
    avg_num = 5
    a = list(range(2 ** p))
    for i in range(avg_num):
        random.shuffle(a)
        s = test_code(fname, a)
        time.append(min(timeit.repeat(setup=s[1], stmt=s[0], repeat=1, number=1)))
    return (sum(time)/avg_num, p, int(c/avg_num))

def exp_1(f, p):
    global c
    arr = list(range(2 ** p))
    fname = f.__name__ 
    s = test_code(fname, arr)
    t = timeit.repeat(setup=s[1], stmt=s[0], repeat=1, number=1)
    return (min(t), p, c)
    
def exp_2(f, p):
    global c
    arr = list(range(2 ** p))
    arr.reverse()
    fname = f.__name__ 
    s = test_code(fname, arr)
    t = timeit.repeat(setup=s[1], stmt=s[0], repeat=1, number=1)
    return (min(t), p, c)

def exp_5(f, p):
    global c
    time = []
    fname = f.__name__ 
    avg_num = 3
    a = [random.randint(1,3) for x in range(2 ** p)]
    for i in range(avg_num):
        random.shuffle(a)
        s = test_code(fname, a)
        time.append(min(timeit.repeat(setup=s[1], stmt=s[0], repeat=1, number=1)))
    return (sum(time)/avg_num, p, int(c/avg_num))

algorithms = [merge_sort, selection_sort, insertion_sort, shell_sort]
colors = ["blue", "mediumvioletred", "green", "orange"]
plot_colors = {algorithms[i].__name__: colors[i] for i in range(len(algorithms))}
experiments = [exp_0, exp_1, exp_2, exp_5]


## Calculating

global c
data = {}
for ex in experiments:
    for powr in range(7, 11):
        for fun in algorithms:
            fname = fun.__name__
            ename = ex.__name__
            if not data.get(ename):
                data.setdefault(ename, {})
            if not data[ename].get(fname):
                data[ename].setdefault(fname, [])
            c = 0
            data[ename][fname].append(ex(fun, powr))


## Plotting data

plots = ['Experiment №0: Random order (Time)',
         'Experiment №0: Random order (Comparisons)',
         'Experiment №1: Increasing order (Time)',
         'Experiment №1: Increasing order (Comparisons)',
         'Experiment №2: Decreasing order (Time)',
         'Experiment №2: Decreasing order (Comparisons)',
         'Experiment №3-5: Avg. random order of {1,2,3} elements',
         'Experiment №3-5: Avg. random order of {1,2,3} elements (Time)']

fig = go.Figure()
fig = make_subplots(rows=4, cols=2, subplot_titles=(plots))
flag = False
for i, e in enumerate(experiments):
    exp = e.__name__
    for f in algorithms:
        fun = f.__name__
        x = [x[1] for x in data[exp][fun]]
        y_c = [x[2] for x in data[exp][fun]]
        y_t = [x[0] for x in data[exp][fun]]
        if i+1 == 1:
            flag = True
        fig.add_trace(go.Scatter(x=x,
                                 y=y_t,
                                 name=fun,
                                 legendgroup=fun,
                                 showlegend=flag,
                                 line_color=plot_colors[fun]),row=i+1,col=1)
        fig.add_trace(go.Scatter(x=x,
                                 y=y_c,
                                 name=fun,
                                 legendgroup=fun,
                                 showlegend=False,
                                 line_color=plot_colors[fun]),row=i+1,col=2)
        fig.update_xaxes(title_text="Number of elements in list", row=i+1, col=1)
        fig.update_yaxes(title_text="Time in seconds", row=1, col=1)
        fig.update_xaxes(title_text="Number of elements in list", row=i+1, col=2)
        fig.update_yaxes(title_text="Comparisons", row=i+1, col=2)
    flag = False
    
fig.update_layout(title_text="Comparing sorting algorithms:", height=1100, width=1000)
fig.show()
