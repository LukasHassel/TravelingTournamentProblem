import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import numpy as np
import pandas as pd

def coefsToLatex(coefs):
    equation = ""
    l = len(coefs)
    for index, c in enumerate(coefs):
        n = (l - index) -1
        if round(c, 3) > 0:
            reprc = f"{'+' if index>0 else''}{round(c, 3):.3f}"
        else:
            reprc = f"{round(c, 3):.3f}"
        if n > 1:
            equation += f" {reprc}x^{n}"
        elif n == 1:
            equation += f" {reprc}x"
        else:
            equation += f" {reprc}"
    return equation

result_file = "output/2026-01-21-10-22-all-results.json"
with open(result_file,'r') as f:
    results = json.load(f)

teamSizes = [i for i in range(4, 52, 2)]

def averageNumberViolations(data:dict[str,int]):
    keys  = [int(key) for key in data.keys()]
    return sum([key * data[str(key)] for key in keys])/sum(data.values())

def maximumNumberViolations(data:dict[str,int]):
    return max(map(int, data.keys()))

def minimumNumberViolations(data:dict[str,int]):
    return min(map(int, data.keys()))

def compute_fit_metrics(x, y, fit_fn):
    x = np.asarray(x)
    y = np.asarray(y)
    y_pred = fit_fn(x)
    residuals = y - y_pred
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2      = 1 - (ss_res / ss_tot) if ss_tot != 0 else float('nan')
    mae     = np.mean(np.abs(residuals))
    mse     = np.mean(residuals ** 2)
    rmse    = np.sqrt(mse)
    max_res = np.max(np.abs(residuals))
    ssr     = ss_res
    return {
        "r2":      r2,
        "mae":     mae,
        "mse":     mse,
        "rmse":    rmse,
        "max_res": max_res,
        "ssr":     ssr,
    }

fig, axs = plt.subplots(ncols=3, nrows=2, figsize=(15, 10), sharey=True, sharex=True, constrained_layout=True)
selector = 0
fit_qualities = []
for noRepeatRounds in range(1,7):
            
    alldrrv = []
    mindrrv = []
    maxdrrv = []

    allmsv = []
    minmsv = []
    maxmsv = []

    allnrv = []
    minnrv = []
    maxnrv = []

    for teamSize in teamSizes:
        currentData = results[f"maxStreak={3};noRepeatRounds={noRepeatRounds}"][f"teams={teamSize}"]

        alldrrv.append(averageNumberViolations(currentData["doubleRoundRobinViolations"]))
        mindrrv.append(minimumNumberViolations(currentData["doubleRoundRobinViolations"]))
        maxdrrv.append(maximumNumberViolations(currentData["doubleRoundRobinViolations"]))

        allmsv.append(averageNumberViolations(currentData["maxStreakViolations"]))
        minmsv.append(minimumNumberViolations(currentData["maxStreakViolations"]))
        maxmsv.append(maximumNumberViolations(currentData["maxStreakViolations"]))
    
        allnrv.append(averageNumberViolations(currentData["noRepeatViolations"]))
        minnrv.append(minimumNumberViolations(currentData["noRepeatViolations"]))
        maxnrv.append(maximumNumberViolations(currentData["noRepeatViolations"]))

    ax = axs[selector//3][selector%3]
    ax.set_ylim(0,2000)
    ax.set_xlim(0, 50)
    
    # Plotting code
    ax.fill_between(teamSizes, mindrrv, maxdrrv, facecolor='salmon')  # 95% CI
    ax.plot(teamSizes, alldrrv, '-', label="All DRRV", color='black')  # All DRRV

    ax.fill_between(teamSizes, minmsv, maxmsv, facecolor='cornflowerblue')  # 95% CI
    ax.plot(teamSizes, allmsv, '-', label="All MSV", color='black')  # All MSV

    ax.fill_between(teamSizes, minnrv, maxnrv, facecolor='gold')  # 95% CI
    ax.plot(teamSizes, allnrv, '-', label="All NRV", color='black')  # All NRV

    fig.supxlabel("Number of Teams")
    fig.supylabel("Number of Violations")
    handles, labels = ax.get_legend_handles_labels()

    drrvfit = np.polyfit(teamSizes, alldrrv, 2)
    drrvfit_fn = np.poly1d(drrvfit)
    fit_qualities.append({
        'noRepeatRounds': noRepeatRounds,
        'violationType' : 'DRRV',
        'LaTeX'  : coefsToLatex(drrvfit_fn.coef),
        **compute_fit_metrics(teamSizes, alldrrv, drrvfit_fn),
    })

    msvfit = np.polyfit(teamSizes, allmsv, 2)
    msvfit_fn = np.poly1d(msvfit)
    fit_qualities.append({
        'noRepeatRounds': noRepeatRounds,
        'violationType' : 'MSV',
        'LaTeX'  : coefsToLatex(msvfit_fn.coef),
        **compute_fit_metrics(teamSizes, allmsv, msvfit_fn),
    })

    nrvfit = np.polyfit(teamSizes, allnrv, 1)
    nrvfit_fn = np.poly1d(nrvfit)
    fit_qualities.append({
        'noRepeatRounds': noRepeatRounds,
        'violationType' : 'NRV',
        'LaTeX'  : coefsToLatex(nrvfit_fn.coef),
        **compute_fit_metrics(teamSizes, allnrv, nrvfit_fn),
    })

    xs = np.linspace(50,100)
    ys = drrvfit_fn(xs)
    fit1, = ax.plot(xs, ys, "--", color='salmon',  label=rf"${coefsToLatex(drrvfit_fn.coef)}$")
    ys = msvfit_fn(xs)
    fit2, = ax.plot(xs, ys, "--", color='cornflowerblue',  label=rf"${coefsToLatex(msvfit_fn.coef)}$")
    ys = nrvfit_fn(xs)
    fit3, = ax.plot(xs, ys, "--", color='gold',  label=rf"${coefsToLatex(nrvfit_fn.coef)}$")
    ax.yaxis.set_label_position("right")
    
    if selector == 0:
        firstLegend = ax.legend([
            mpatches.Patch(color="salmon"),
            mpatches.Patch(color="cornflowerblue"),
            mpatches.Patch(color="gold"),
            mlines.Line2D([0], [0], color='black'),
        ], 
        [
            "Double Round-Robin",
            "maxStreak",
            "noRepeat",
            "Average",
        ], loc=(0.05, 0.65))#, prop={'weight':'bold'})
    ax.text(20, 1800, f"noRepeat = {noRepeatRounds}", bbox={'facecolor':'lightgrey'}, fontweight="bold")

    if selector == 0:
        ax.text(27, 500, rf"${coefsToLatex(drrvfit_fn.coef)}$", bbox={'facecolor':'salmon'})
    else:
        ax.text(25, 1500, rf"${coefsToLatex(drrvfit_fn.coef)}$", bbox={'facecolor':'salmon'})
    ax.text(2, 400, rf"${coefsToLatex(msvfit_fn.coef)}$", bbox={'facecolor':'cornflowerblue'})
    
    if selector < 3:
        ax.text(30, 110, rf"${coefsToLatex(nrvfit_fn.coef)}$", bbox={'facecolor':'gold'})
    else:
        ax.text(30, 400, rf"${coefsToLatex(nrvfit_fn.coef)}$", bbox={'facecolor':'gold'})

    fig.tight_layout()
    selector += 1

plt.savefig(f"figures/fit_noRepeats.png")
pd.DataFrame(fit_qualities).to_csv("figures/fit_qualities.csv", index=False)