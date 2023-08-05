import { color } from 'd3-color';
import { scaleDiverging, scaleOrdinal, scaleSequential } from 'd3-scale';
import {
  interpolateBlues,
  interpolateBrBG,
  interpolateBuGn,
  interpolateBuPu,
  interpolateCividis,
  interpolateCool,
  interpolateGnBu,
  interpolateGreens,
  interpolateGreys,
  interpolateInferno,
  interpolateMagma,
  interpolateOranges,
  interpolateOrRd,
  interpolatePiYG,
  interpolatePlasma,
  interpolatePRGn,
  interpolatePuBu,
  interpolatePuBuGn,
  interpolatePuOr,
  interpolatePuRd,
  interpolatePurples,
  interpolateRainbow,
  interpolateRdBu,
  interpolateRdGy,
  interpolateRdPu,
  interpolateRdYlBu,
  interpolateRdYlGn,
  interpolateReds,
  interpolateSinebow,
  interpolateSpectral,
  interpolateTurbo,
  interpolateViridis,
  interpolateWarm,
  interpolateYlGn,
  interpolateYlGnBu,
  interpolateYlOrBr,
  interpolateYlOrRd,
  schemeAccent,
  schemeCategory10,
  schemeDark2,
  schemePaired,
  schemePastel1,
  schemePastel2,
  schemeSet1,
  schemeSet2,
  schemeSet3,
  schemeTableau10
} from 'd3-scale-chromatic';

export const colormapFactories = {
  seq: {
    Blues: () => scaleSequential(interpolateBlues),
    Greens: () => scaleSequential(interpolateGreens),
    Greys: () => scaleSequential(interpolateGreys),
    Oranges: () => scaleSequential(interpolateOranges),
    Purples: () => scaleSequential(interpolatePurples),
    Reds: () => scaleSequential(interpolateReds),
    Turbo: () => scaleSequential(interpolateTurbo),
    Viridis: () => scaleSequential(interpolateViridis),
    Inferno: () => scaleSequential(interpolateInferno),
    Magma: () => scaleSequential(interpolateMagma),
    Plasma: () => scaleSequential(interpolatePlasma),
    Cividis: () => scaleSequential(interpolateCividis),
    Warm: () => scaleSequential(interpolateWarm),
    Cool: () => scaleSequential(interpolateCool),
    BuGn: () => scaleSequential(interpolateBuGn),
    BuPu: () => scaleSequential(interpolateBuPu),
    GnBu: () => scaleSequential(interpolateGnBu),
    OrRd: () => scaleSequential(interpolateOrRd),
    PuBuGn: () => scaleSequential(interpolatePuBuGn),
    PuBu: () => scaleSequential(interpolatePuBu),
    PuRd: () => scaleSequential(interpolatePuRd),
    RdPu: () => scaleSequential(interpolateRdPu),
    YlGnBu: () => scaleSequential(interpolateYlGnBu),
    YlGn: () => scaleSequential(interpolateYlGn),
    YlOrBr: () => scaleSequential(interpolateYlOrBr),
    YlOrRd: () => scaleSequential(interpolateYlOrRd),
    Rainbow: () => scaleSequential(interpolateRainbow),
    Sinebow: () => scaleSequential(interpolateSinebow)
  },
  div: {
    BrBG: () => scaleDiverging(interpolateBrBG),
    PRGn: () => scaleDiverging(interpolatePRGn),
    PiYG: () => scaleDiverging(interpolatePiYG),
    PuOr: () => scaleDiverging(interpolatePuOr),
    RdBu: () => scaleDiverging(interpolateRdBu),
    RdGy: () => scaleDiverging(interpolateRdGy),
    RdYlBu: () => scaleDiverging(interpolateRdYlBu),
    RdYlGn: () => scaleDiverging(interpolateRdYlGn),
    Spectral: () => scaleDiverging(interpolateSpectral)
  },
  cat: {
    Category10: () => scaleOrdinal(schemeCategory10),
    Accent: () => scaleOrdinal(schemeAccent),
    Dark2: () => scaleOrdinal(schemeDark2),
    Paired: () => scaleOrdinal(schemePaired),
    Pastel1: () => scaleOrdinal(schemePastel1),
    Pastel2: () => scaleOrdinal(schemePastel2),
    Set1: () => scaleOrdinal(schemeSet1),
    Set2: () => scaleOrdinal(schemeSet2),
    Set3: () => scaleOrdinal(schemeSet3),
    Tableau10: () => scaleOrdinal(schemeTableau10)
  }
};

// Transform a d3 color '#abcdef' to numeric #abcdef that pixi uses
export function colorToNumber(c) {
  c = color(c);
  if (c) {
    return parseInt(c.formatHex().slice(1), 16);
  }
  return 0;
}
