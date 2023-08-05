"""Plot a matplotlib fig on a tkinter widget win (tkinter.Tk() or tkinter.Frame)."""
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


def tk_plot(
    fig: matplotlib.figure.Figure,
    win: tk.Tk = None,
    title: str = "",
    toolbar: bool = True,
) -> FigureCanvasTkAgg:
    r"""Plot matplotlib figues in a tkinter.Tk/Frame.

    Args:
        fig: matplotlib figure
        win: tkinter.Tk() or tkinter.Frame()
        title: tkinter widget title
        toolbar: if set to True, a toolbar (matplotlib toolbar) is shown

    Returns:
        canvas: a FigureCanvasTkAgg, run canvas.draw() to update.

    snippets\tkinter drawfig*.py (PySimpleGUi matplotlib exampl)
    matplotlib cookbook: Embedding Matplotlib in a Tkinter GUI application

    matplotlib.use('TkAgg')

    import seaborn as sns
    sns.set_theme()
    sns.set_style("whitegrid")
    matplotlib.pyplot.ion()  # for testing in ipython

    from matplotlib.gridspec import GridSpec
    gs = GridSpec(3, 1)
    """
    if win is None:
        win = tk.Tk()
    if title:
        win.wm_title(title)
    else:
        win.wm_title("Fig in Tk")

    canvas = FigureCanvasTkAgg(fig, win)
    canvas.get_tk_widget().pack(side="top", fill="both", expand=1)
    if toolbar:
        NavigationToolbar2Tk(canvas, win)

    tk_plot.win = win
    # tk_plot.win.destroy() to exit

    return canvas


def main(root):
    """Run."""
    win = ttk.Frame(root)
    win.pack()

    fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)

    canvas = tk_plot(fig)

    # canvas = tk_plot(fig, win)

    canvas.draw()

    _ = """
    # update fig
    ax1 = fig.add_subplot(211)  # gs[,] gs = mpl.gridspec.GridSpec(3,1)
    # ax1.plot(...) or sns.heatmap(ax=ax1), df.plot(..., ax=ax)
    canvas.draw()

    # fig.clear()  # fig.clf()
    # axes = fig.axes

    """


if __name__ == "__main__":
    root = tk.Tk()
    main(root)
    root.mainloop()
