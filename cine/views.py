from django.http import HttpResponse
from django.shortcuts import render_to_response

from bom import BOM, DAILY_CHART, WEEKEND_CHART, WEEKLY_CHART

import time, random, datetime

def index(request, title=DAILY_CHART):
    bom = BOM(title)

    if title == WEEKEND_CHART:
        _chart = 'Weekend Charts'
    elif title == WEEKLY_CHART:
        _chart = 'Weekly Charts'
    else:
        _chart = 'Daily Charts'


    movies = request.session.get(_chart, False)

    if not movies:
        movies = bom.get_chart()

    xdata = []
    titles = []
    ydata = []
    ranks = []
    mvs = []

    for (i, m) in enumerate(movies):
        xdata.append(i+1)
        titles.append(str(m.title))
        ydata.append(m.gross_val)
        ranks.append({'title':m.title, 'rank':m.rank})
        mvs.append(m)

        request.session[m.movie_id] = m.movie_id

    request.session[_chart] = mvs

    extra_serie = {"tooltip": {"y_start": "$", "y_end": ""}}

    kw_extra = {
        'show_legend': False,
        'show_labels': False,
        'color_category': 'category20'
    }

    chartdata = {
        'x': xdata,
        #'name1': 'Weekend Box Office Charts',
        #'y1': ydata, 'extra1': extra_serie,
        #'y2': ydata, 'extra2': extra_serie
        #'kwargs': kwargs
    }
    
    for i in range(0, len(xdata)):
        chartdata['name%d' % (i+1)] = titles[i]
        chartdata['y%d' % (i+1)] = [ydata[i]]
        chartdata['extra%d' % (i+1)] = extra_serie
    
    charttype = "multiBarHorizontalChart"
    chartcontainer = "multibarhorizontalchart_container"
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'height': '80%', 'width': '100%',
        'kw_extra': kw_extra,
        'movies': mvs,
        'chart': _chart,
        'title': title,
        'date': bom.date
    }

    return render_to_response('index.html', data)

def movie(request, movie_id):
    """
    lineChart page
    """
    start_time = int(time.mktime(datetime.datetime(2012, 6, 1).timetuple()) * 1000)
    nb_element = 150
    xdata = range(nb_element)
    xdata = map(lambda x: start_time + x * 1000000000, xdata)
    ydata = [i + random.randint(1, 10) for i in range(nb_element)]
    ydata2 = map(lambda x: x * 2, ydata)

    tooltip_date = "%d %b %Y %H:%M:%S %p"
    extra_serie1 = {
        "tooltip": {"y_start": "", "y_end": " cal"},
        "date_format": tooltip_date,
        'color': '#a4c639'
    }
    extra_serie2 = {
        "tooltip": {"y_start": "", "y_end": " cal"},
        "date_format": tooltip_date,
        'color': '#FF8aF8'
    }
    chartdata = {'x': xdata,
                 'name1': 'series 1', 'y1': ydata, 'extra1': extra_serie1,
                 'name2': 'series 2', 'y2': ydata2, 'extra2': extra_serie2}

    charttype = "lineChart"
    chartcontainer = 'linechart_container'  # container name
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'kw_extra': {
            'x_is_date': True,
            'x_axis_format': '%d %b %Y %H',
            'tag_script_js': True,
            'jquery_on_ready': False,
        },
        'height': '80%', 'width': '100%'
    }
    return render_to_response('movie.html', data)
