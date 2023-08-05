<script>
  import { getContext } from 'svelte';
  import { scaleSqrt } from 'd3-scale';
  import { extent } from 'd3-array';
  import Slider from '@bulatdashiev/svelte-slider';
  import { colormapFactories, colorToNumber } from '../../util/colors';

  // --- Component props
  export let dataKey = null;
  export let encodingKey = null;
  export let nodeMappingKey = null;
  export let receive = null;
  export let send = null;
  export let visible = '';

  // --- Contexts
  const { nodes, featureMode } = getContext(dataKey);
  const { nodeColors, nodeRadii } = getContext(encodingKey);
  const { mapColor, colorType, colorScale, mapSize, sizeScale } =
    getContext(nodeMappingKey);

  // --- UI variables
  let colorMapOptions = Object.keys(colormapFactories[$colorType]);
  let colorMap = $featureMode ? 'Turbo' : 'Viridis';
  let colorDomain = [-2, 2];
  let cmin = -1;
  let cmid = 0;
  let cmax = 1;
  let sizeDomain = [0, 1];
  let smin = 0;
  let smax = 1;
  let sizeRange = [2, 5];
  let sizeRange_ = sizeRange;

  $colorScale = colormapFactories[$colorType][colorMap]();
  $sizeScale = scaleSqrt().clamp(true);

  // --- Reactive processes
  // New data
  $: {
    // Depending on the entire nodes object-array to detect changes in color-data
    // and radius-data means that we cannot prevent the layout from re-starting
    // when only color-data is changed. Best solution is to communicate what
    // changed from the server (python), otherwise we need (expensive) array
    // comparisons to check what changed here.
    console.log('new nodes data for mapping');
    updateColorDomain($nodes, $featureMode);
    updateSizeDomain($nodes, $featureMode);
    applyDomains();
    computeColors();
    computeSizes();
  }

  // New color type
  $: {
    // Change available color maps
    // Update color_domain for new type
    // triggers changed color map reaction
    updateColormapType($colorType, $featureMode);
  }
  // Changed color map
  $: {
    // Create new color_scale and apply domain
    updateColorMap(colorMap);
    computeColors();
  }
  // Changed domain through ui
  $: {
    // Update the domain
    // Apply domain to color_scale
    updateColorDomainUI(cmin, cmid, cmax);
    computeColors();
  }
  // Changed size domain or range through ui
  $: {
    // Update size_domain
    updateSizeDomainUI(smin, smax);
    computeSizes();
  }
  $: {
    // Update size range unfortunately, this block is called everytime
    // the range slider is constructed, causing a restart of the layout simulation
    // So the computeSizesConditional adds a check whether the size range actually
    // changed compared to last time.
    updateSizeRangeUI(sizeRange);
    computeSizesConditional();
  }

  function updateColorDomain(nodes_, mode) {
    const colorData = nodes_.map((n) => n.color_data);
    if ($colorType === 'cat') {
      const uniqueValue = [...new Set(colorData)];
      colorDomain = uniqueValue.sort((a, b) => a - b);
      $mapColor = colorDomain.length > 1;
      return;
    }

    const [cmin_, cmax_] = extent(colorData);
    $mapColor = cmin_ !== cmax_;
    if (mode) {
      colorDomain = [-2, 2];
      [cmin, cmax] = colorDomain;
    } else {
      [cmin, cmax] = [cmin_, cmax_];
      if ($colorType === 'seq') {
        colorDomain = [cmin, cmax];
      } else {
        // color_type === 'div'
        cmid = colorData.reduce((a, b) => a + b, 0) / colorData.length;
        colorDomain = [cmin, cmid, cmax];
      }
    }
  }

  function updateSizeDomain(nodes_, mode) {
    const [smin_, smax_] = extent(nodes_.map((n) => n.radius_data));
    if (mode) {
      sizeDomain = [0, 1];
      [smin, smax] = sizeDomain;
    } else {
      sizeDomain = [smin_, smax_];
      [smin, smax] = sizeDomain;
    }
    const oldMapSize = mapSize;
    $mapSize = smin_ !== smax_;
    if (oldMapSize !== $mapSize) {
      if ($mapSize) {
        sizeRange = [1, 5];
      } else {
        sizeRange = [4, 5];
      }
    }
  }

  function applyDomains() {
    $sizeScale.domain(sizeDomain).nice();
    $colorScale.domain(colorDomain);
    if ($colorType !== 'cat') {
      $colorScale.nice();
    }
  }

  function computeSizes() {
    if (!$mapSize) {
      $nodeRadii = $nodes.map(() => sizeRange[0]);
    } else {
      $nodeRadii = $nodes.map((n) => $sizeScale(n.radius_data));
    }
    $sizeScale = $sizeScale; // Trigger legend update!
  }

  function computeColors() {
    $nodeColors = $nodes.map((n) => colorToNumber($colorScale(n.color_data)));
    $colorScale = $colorScale; // Triggers legend update!
  }

  function updateColormapType(type, mode) {
    colorMapOptions = Object.keys(colormapFactories[type]);
    if (type === 'seq') {
      colorMap = mode ? 'Turbo' : 'Viridis';
    } else {
      colorMap = colorMapOptions[0];
    }

    updateColorDomain($nodes);
  }

  function updateColorMap(mapName) {
    $colorScale = colormapFactories[$colorType][mapName]();
    $colorScale.domain(colorDomain);
    if ($colorType !== 'cat') {
      $colorScale.nice();
    }
  }

  function updateColorDomainUI(min, mid, max) {
    if ($colorType === 'cat') {
      return;
    }
    if ($colorType === 'div') {
      colorDomain = [min, mid, max];
    } else {
      colorDomain = [min, max];
    }
    $colorScale.domain(colorDomain).nice();
  }

  function updateSizeDomainUI(min, max) {
    sizeDomain = [min, max];
    $sizeScale.domain(sizeDomain).nice();
  }

  function updateSizeRangeUI(range) {
    $sizeScale.range(range).nice();
  }

  function computeSizesConditional() {
    if (sizeRange[0] === sizeRange_[0] && sizeRange[1] === sizeRange_[1]) {
      return;
    }
    sizeRange_ = sizeRange;
    computeSizes();
  }
</script>

{#if visible === 'node'}
  <div
    id="node-mapping-container"
    in:receive={{ key: 'node' }}
    out:send={{ key: 'node' }}>
    <b>Color</b>
    <buttton id="close-button" on:click={() => (visible = '')}>
      <span>&times;</span>
    </buttton>
    <label>
      Type:
      <select bind:value={$colorType}>
        <option value="seq">Sequential</option>
        <option value="div">Diverging</option>
        <option value="cat">Categorical</option>
      </select>
    </label>
    <label>
      Map:
      <select bind:value={colorMap}>
        {#each colorMapOptions as map}
          <option value={map}>{map}</option>
        {/each}
      </select>
    </label>
    <div class="row">
      <span class={$colorType === 'div' ? 'third' : 'half'}>Min:</span>
      {#if colorType === 'div'}
        <span class="third">Mid:</span>
      {/if}
      <span class={$colorType === 'div' ? 'third' : 'half'}>Max:</span>
    </div>
    <div class="row">
      <input
        class={$colorType === 'div' ? 'third' : 'half'}
        disabled={$colorType === 'cat'}
        type="number"
        bind:value={cmin} />
      {#if $colorType === 'div'}
        <input class="third" type="number" bind:value={cmid} />
      {/if}
      <input
        class={$colorType === 'div' ? 'third' : 'half'}
        disabled={$colorType === 'cat'}
        type="number"
        bind:value={cmax} />
    </div>

    <b>Size</b>
    <span>Domain:</span>
    <div class="row">
      <input class="half" type="number" bind:value={smin} />
      <input class="half" type="number" bind:value={smax} />
    </div>
    <span>Range:</span>
    <Slider
      bind:value={sizeRange}
      range={$mapSize}
      order
      min="0"
      max="10"
      step="0.1" />
  </div>
{/if}

<style>
  .row {
    display: flex;
    flex-direction: row;
  }

  .half {
    width: 50%;
  }

  .third {
    width: 33%;
  }

  #node-mapping-container {
    position: absolute;
    top: 10px;
    left: 10px;
    width: 180px;
    margin: 5px;
    padding: 5px;
    border: 2px solid #ffffff;
    border-radius: 5px;
    display: flex;
    flex-direction: column;
    color: rgb(50, 50, 50);
  }

  #close-button {
    background-color: #eeeeee;
    position: absolute;
    cursor: pointer;
    border: none;
    border-radius: 50%;
    right: 1%;
    top: 1%;
    width: 15px;
    height: 15px;
    line-height: 15px;
    text-align: center;
  }

  #close-button span {
    top: -1px;
    display: inline;
    position: relative;
  }

  select {
    border-radius: 4px;
    background-color: #fff;
    border: 1px solid #ccc;
    color: #333;
    height: 25px;
    width: 55%;
  }

  input[type='number'] {
    border-radius: 4px;
    background-color: #fff;
    border: 1px solid #ccc;
    color: #333;
    height: 25px;
    padding-left: 2px;
  }

  select,
  input {
    font-family: Arial;
    font-size: 13px;
    line-height: normal;
    margin: 1px;
    padding: 1px;
  }
</style>
