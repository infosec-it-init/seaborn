from __future__ import annotations
from dataclasses import dataclass

import numpy as np
import matplotlib as mpl

from seaborn._marks.base import (
    Mark,
    Mappable,
    MappableFloat,
    MappableString,
    MappableColor,
    resolve_properties,
)


# TODO the collection of marks defined here is a holdover from very early
# "let's just got some plots on the screen" phase. They should maybe go elsewhere.


@dataclass
class Line(Mark):
    """
    A mark connecting data points with sorting along the orientation axis.
    """

    # TODO other semantics (marker?)

    color: MappableColor = Mappable("C0", )
    alpha: MappableFloat = Mappable(1, )
    linewidth: MappableFloat = Mappable(rc="lines.linewidth", )
    linestyle: MappableString = Mappable(rc="lines.linestyle", )

    # TODO alternately, have Path mark that doesn't sort
    sort: bool = True

    def _plot(self, split_gen, scales, orient):

        for keys, data, ax in split_gen(dropna=False):

            keys = resolve_properties(self, keys, scales)

            if self.sort:
                # TODO where to dropna?
                data = data.sort_values(orient)
            else:
                data.loc[data.isna().any(axis=1), ["x", "y"]] = np.nan

            line = mpl.lines.Line2D(
                data["x"].to_numpy(),
                data["y"].to_numpy(),
                color=keys["color"],
                alpha=keys["alpha"],
                linewidth=keys["linewidth"],
                linestyle=keys["linestyle"],
                **self.artist_kws,  # TODO keep? remove? be consistent across marks
            )
            ax.add_line(line)

    def _legend_artist(self, variables, value, scales):

        key = resolve_properties(self, {v: value for v in variables}, scales)

        return mpl.lines.Line2D(
            [], [],
            color=key["color"],
            alpha=key["alpha"],
            linewidth=key["linewidth"],
            linestyle=key["linestyle"],
        )
