<script>
  import { select } from 'd3-selection';
  import { axisBottom } from 'd3-axis';
  import { scaleLinear } from 'd3-scale';
  import { quantile, range } from 'd3-array';
  import { interpolate, quantize } from 'd3-interpolate';
  import { onDestroy } from 'svelte';

  // --- Component props
  export let scale = null;
  export let viewport = null;
  export let shape = 'circle'; // or 'line'
  export let tickSize = 6;
  export let width = 320;
  export let height = 34 + tickSize;
  export let marginTop = 5;
  export let marginRight = 10;
  export let marginBottom = 16 + tickSize;
  export let marginLeft = 5;
  export let ticks = width / 32;
  export let tickFormat = null;
  // export let tickValues = null;

  // --- The tick svg group
  let g = null;
  const line_length = (width - marginLeft - marginRight) / ticks;

  // Account for pixi viewport zoom level
  let ratio = viewport.screenWorldHeight / viewport.worldHeight;
  viewport.on('wheel', computeZoomRatio);

  function computeZoomRatio() {
    ratio = viewport.screenWorldHeight / viewport.worldHeight;
  }

  // --- Compute tick-values
  $: domain = $scale.domain();
  $: tickValues = range(ticks + 1).map((i) => quantile(domain, i / ticks));

  $: x_scale = scaleLinear()
    .domain(domain)
    .rangeRound(quantize(interpolate(marginLeft, width - marginRight), 2));

  $: x_axis = axisBottom(x_scale)
    .ticks(ticks, typeof tickFormat === 'string' ? tickFormat : null)
    .tickFormat(typeof tickFormat === 'function' ? tickFormat : null)
    .tickSize(tickSize)
    .tickValues(tickValues);

  $: data = range(tickValues.length).map((i) => {
    return {
      x: x_scale(tickValues[i]) + 0.5,
      r: ratio * $scale(tickValues[i])
    };
  });

  $: if (g) {
    select(g)
      .call((g) => g.selectAll('.tick').remove())
      .call(x_axis)
      .call((g) =>
        g.selectAll('.tick line').attr('y1', marginTop + marginBottom - height)
      )
      .call((g) => g.select('.domain').remove());
  }

  // --- Lifetime
  onDestroy(() => {
    viewport.off('wheel', computeZoomRatio);
  });
</script>

<svg
  class="size-legend"
  height={height}
  viewbox={[0, 0, width, height]}
  width={width}>
  <g bind:this={g} transform={`translate(0,${height - marginBottom})`} />
  <g transform={`translate(0,${height - marginBottom})`}>
    {#if shape === 'circle'}
      {#each data as { x, r }}
        <circle
          cx={x}
          cy={marginTop + marginBottom - height + tickSize}
          r={r}
          fill="#fff"
          stroke="#ccc"
          stroke-width="1" />
      {/each}
    {:else}
      {#each data as { x, r }}
        <line
          stroke="#fff"
          stroke-width={r}
          y1={(marginTop + marginBottom - height + tickSize) / 2}
          y2={(marginTop + marginBottom - height + tickSize) / 2}
          x1={x - line_length / 3}
          x2={x + line_length / 3} />
      {/each}
    {/if}
  </g>
</svg>

<style>
  .size-legend {
    overflow: visible;
    display: block;
  }
</style>
