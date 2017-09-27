import json
import datetime
import numpy as np


def getFinalJSON(submissionId):
    dict = {}
    # import pdb; pdb.set_trace()
    for i in range(3):
        fileName = submissionId + 'result' + str(i+1) + '.json'
        with open(fileName) as json_data:
            dict[i] = json.load(json_data)

    results = {}

    timediff1 = datetime.datetime.strptime(dict[1]['dates'][-1], '%Y-%m-%dT%H:%M:%S.000000000') - \
        datetime.datetime.strptime(dict[0]['dates'][0], '%Y-%m-%dT%H:%M:%S.000000000')
    timediff2 = datetime.datetime.strptime(dict[0]['dates'][-1], '%Y-%m-%dT%H:%M:%S.000000000') - \
        datetime.datetime.strptime(dict[2]['dates'][0], '%Y-%m-%dT%H:%M:%S.000000000')
    dates = [datetime.datetime.strptime(i, '%Y-%m-%dT%H:%M:%S.000000000') for i in dict[1]['dates']]
    dates = dates + [datetime.datetime.strptime(i, '%Y-%m-%dT%H:%M:%S.000000000') + timediff1 + datetime.timedelta(hours=22) for i in dict[0]['dates']]
    dates = dates + [datetime.datetime.strptime(i, '%Y-%m-%dT%H:%M:%S.000000000') + timediff1 + datetime.timedelta(hours=22) + timediff2 + datetime.timedelta(hours=23) for i in dict[2]['dates']]
    total_pnl = dict[1]['total_pnl'] + \
        [x + dict[1]['total_pnl'][-1] for x in dict[0]['total_pnl']] + \
        [x + dict[1]['total_pnl'][-1] + dict[0]['total_pnl'][-1] for x in dict[2]['total_pnl']]
    results['dates'] = [str(i) for i in dates]
    results['total_pnl'] = total_pnl
    results['instrument_names'] = dict[0]['instrument_names']
    results['instrument_stats'] = []
    score = 0
    for i in range(len(dict[0]['instrument_names'])):
        iDict = {}
        iDict['total_pnl'] = '%.3f' % (100 * sum([dict[0]['instrument_stats'][i]['total_pnl'],
                                                  dict[1]['instrument_stats'][i]['total_pnl'],
                                                  dict[2]['instrument_stats'][i]['total_pnl']]))
        iDict['score'] = np.sqrt(sum([dict[0]['instrument_stats'][i]['score']**2,
                                      dict[1]['instrument_stats'][i]['score']**2,
                                      dict[2]['instrument_stats'][i]['score']**2]) / 3.0)
        iDict['dataset1_score'] = '%.3f' % dict[0]['instrument_stats'][i]['score']
        iDict['dataset2_score'] = '%.3f' % dict[1]['instrument_stats'][i]['score']
        iDict['dataset3_score'] = '%.3f' % dict[2]['instrument_stats'][i]['score']
        benchmark_score = np.sqrt(sum([(dict[0]['instrument_stats'][i]['score'] / dict[0]['instrument_stats'][i]['normalized_score'])**2,
                                       (dict[1]['instrument_stats'][i]['score'] / dict[1]['instrument_stats'][i]['normalized_score'])**2,
                                       (dict[2]['instrument_stats'][i]['score'] / dict[2]['instrument_stats'][i]['normalized_score'])**2]) / 3.0)
        score = score + iDict['score'] / benchmark_score
        iDict['score'] = '%.3f' % iDict['score']
        results['instrument_stats'].append(iDict)

    results['metrics_values'] = []
    results['metrics'] = []
    idx0 = dict[0]['metrics'].index('Total Pnl(%)')
    results['metrics'].append('Total Pnl(%)')
    results['metrics_values'].append(100 * sum([dict[0]['metrics_values'][idx0], dict[1]['metrics_values'][idx0], dict[2]['metrics_values'][idx0]]))
    idx1 = dict[0]['metrics'].index('Profit/Loss Ratio')
    totalLoss = sum([dict[0]['metrics_values'][idx0] / (dict[0]['metrics_values'][idx1] - 1),
                     dict[1]['metrics_values'][idx0] / (dict[1]['metrics_values'][idx1] - 1),
                     dict[2]['metrics_values'][idx0] / (dict[2]['metrics_values'][idx1] - 1)])
    totalProfit = sum([dict[0]['metrics_values'][idx1] * dict[0]['metrics_values'][idx0] / (dict[0]['metrics_values'][idx1] - 1),
                       dict[1]['metrics_values'][idx1] * dict[1]['metrics_values'][idx0] / (dict[1]['metrics_values'][idx1] - 1),
                       dict[2]['metrics_values'][idx1] * dict[2]['metrics_values'][idx0] / (dict[2]['metrics_values'][idx1] - 1)])
    results['metrics'].append('Profit/Loss Ratio')
    results['metrics_values'].append(totalProfit / totalLoss)
    idx = dict[0]['metrics'].index('Max Drawdown(%)')
    results['metrics'].append('Max Drawdown(%)')
    results['metrics_values'].append(100 * max([dict[0]['metrics_values'][idx], dict[1]['metrics_values'][idx], dict[2]['metrics_values'][idx]]))
    idx = dict[0]['metrics'].index('Accuracy')
    results['metrics'].append('Accuracy')
    results['metrics_values'].append(sum([dict[0]['metrics_values'][idx], dict[1]['metrics_values'][idx], dict[2]['metrics_values'][idx]]) / 3.0)
    results['metrics'].append('Score')
    results['metrics_values'].append(score / float(len(results['instrument_names'])))
    idx = dict[0]['metrics'].index('Score')
    results['metrics'].append('Dataset 1 Score')
    results['metrics_values'].append(dict[0]['metrics_values'][idx])
    results['metrics'].append('Dataset 2 Score')
    results['metrics_values'].append(dict[1]['metrics_values'][idx])
    results['metrics'].append('Dataset 3 Score')
    results['metrics_values'].append(dict[2]['metrics_values'][idx])
    # sum([dict[0]['metrics'][idx], dict[1]['metrics'][idx], dict[2]['metrics'][idx]]) / 3.0
    results['score'] = score / float(len(results['instrument_names']))

    return results
