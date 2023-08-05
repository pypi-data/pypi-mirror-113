<script>
  import { getContext } from 'svelte';
  import { scaleLinear } from 'd3-scale';
  import { extent } from 'd3-array';
  import Slider from '@bulatdashiev/svelte-slider';
  import { colormapFactories, colorToNumber } from '../../util/colors';

  // --- Component props
  export let dataKey = null;
  export let encodingKey = null;
  export let edgeMappingKey = null;
  export let receive = null;
  export let send = null;
  export let visible = '';

  // --- Contexts
  const { edges } = getContext(dataKey);
  const { edgeColors, edgeWidths, edgeAlpha } = getContext(encodingKey);
  const { mapColor, colorType, colorScale, mapSize, sizeScale } =
    getContext(edgeMappingKey);

  // --- UI variables
  let colorMapOptions = Object.keys(colormapFactories[$colorType]);
  let colorMap = colorMapOptions[2];
  let colorDomain = [0, 1];
  let cmin = 0;
  let cmid = 0.5;
  let cmax = 1;
  let sizeDomain = [0, 1];
  let smin = 0;
  let smax = 1;
  let sizeRange = [2, 5];
  let sizeRange_ = sizeRange;
  let edgeAlpha_ = [0.1];
  

  $colorScale = colormapFactories[$colorType][colorMap]();
  $sizeScale = scaleLinear().clamp(true);
  

  // --- Reactive processes
  // New data
  $: {
    console.log('new edge data for mapping');
    updateColorDomain($edges);
    updateSizeDomain($edges);
    applyDomains();
    computeColors();
    computeSizes();
  }

  // New color type
  $: {
    // Change available color maps
    // Update color_domain for new type
    // triggers changed color map reaction
    updateColormapType($colorType);
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
  $: $edgeAlpha = edgeAlpha_[0]

  function updateColorDomain(edges_) {
    const colorData = edges_.map((e) => e.color_data);
    if ($colorType === 'cat') {
      const uniqueValue = [...new Set(colorData)];
      colorDomain = uniqueValue.sort((a, b) => a - b);
      $mapColor = colorDomain.length > 1;
      return;
    }

    [cmin, cmax] = extent(colorData);
    $mapColor = cmin !== cmax;
    if ($colorType === 'seq') {
      colorDomain = [cmin, cmax];
    } else {
      // color_type === 'div'
      cmid = colorData.reduce((a, b) => a + b, 0) / colorData.length;
      colorDomain = [cmin, cmid, cmax];
    }
  }

  function updateSizeDomain(edges_) {
    sizeDomain = extent(edges_.map((e) => e.width_data));
    [smin, smax] = sizeDomain;
    const oldMapSize = mapSize;
    $mapSize = smin !== smax;
    if (oldMapSize !== $mapSize) {
      if (mapSize) {
        sizeRange = [1, 5];
      } else {
        sizeRange = [2, 5];
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
      $edgeWidths = $edges.map(() => sizeRange[0]);
    } else {
      $edgeWidths = $edges.map((e) => $sizeScale(e.width_data));
    }
    $sizeScale = $sizeScale; // Trigger legend update!
  }

  function computeColors() {
    $edgeColors = $edges.map((e) => colorToNumber($colorScale(e.color_data)));
    $colorScale = $colorScale; // Triggers legend update!
  }

  function updateColormapType(type) {
    colorMapOptions = Object.keys(colormapFactories[type]);
    colorMap = colorMapOptions[2];
    updateColorDomain($edges);
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

{#if visible === 'edge'}
  <div
    id="edge-mapping-container"
    in:receive={{ key: 'edge' }}
    out:send={{ key: 'edge' }}>
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
    <span>Alpha:</span>
    <Slider
      bind:value={edgeAlpha_}
      range={false}
      min="0"
      max="1"
      step="0.02" />
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

  #edge-mapping-container {
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
