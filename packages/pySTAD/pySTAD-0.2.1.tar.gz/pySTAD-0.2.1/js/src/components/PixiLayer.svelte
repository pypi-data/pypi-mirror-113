<script>
  import { onDestroy, onMount, setContext, getContext } from 'svelte';
  import { writable } from 'svelte/store';
  import { Application, Point } from 'pixi.js';
  import { Viewport } from 'pixi-viewport';
  import LegendsLayer from './legends/LegendsLayer.svelte';
  import NodesLayer from './network/NodesLayer.svelte';
  import EdgesLayer from './network/EdgesLayer.svelte';
  import ProgressBar from './network/ProgressBar.svelte';
  import PixiLasso from './network/PixiLasso.svelte';

  // --- Component props
  export let dataKey = null;
  export let encodingKey = null;
  export let nodeMappingKey = null;
  export let edgeMappingKey = null;
  export let worldHeight = 10;
  export let worldWidth = 10;
  export let defaultZoomScale = 1;
  export let minZoomScale = 0.01;
  export let maxZoomScale = 100;
  export let initialWidth = 750;
  export let initialHeight = 450;

  // --- General variables
  let element = null;
  let renderId = null;
  const { featureMode } = getContext(dataKey);

  // --- Pixi Context
  const renderKey = {};
  const width = writable(0);

  // Configure Pixi app
  const app = new Application({
    width: initialWidth,
    height: initialHeight,
    resolution: window.devicePixelRatio || 1,
    transparent: true,
    antialias: true,
    autoStart: false
  });
  app.view.addEventListener('wheel', (event) => {
    event.preventDefault();
  });
  app.renderer.autoResize = true;
  app.renderer.view.style.backgroundColor = '#ddd';

  // Configure Pixi viewport
  const viewport = new Viewport({
    screenWidth: initialWidth,
    screenHeight: initialHeight,
    worldWidth: worldWidth,
    worldHeight: worldHeight,
    interaction: app.renderer.plugins.interaction
  });
  // Enable interactions
  viewport
    .drag()
    .pinch()
    .wheel()
    .clampZoom({ minScale: minZoomScale, maxScale: maxZoomScale })
    .setZoom(defaultZoomScale, true);
  viewport.center = new Point(0, 0);
  viewport.on('frame-end', renderAnimation);
  // Add viewport to the PixiApplication
  app.stage.addChild(viewport);

  setContext(renderKey, {
    app: app,
    viewport: viewport,
    width: width,
    requestRender: requestRender
  });

  // --- Lifetime

  onMount(() => {
    console.log('mount pixi application');
    resizeApplication($width);
    element.appendChild(app.renderer.view);
  });

  onDestroy(() => {
    console.log('destroy pixi application');
    if (renderId) {
      cancelAnimationFrame(renderId);
    }
    app.destroy(true, true);
    viewport.off('frame-end', renderAnimation);
    viewport.destroy(true);
  });

  // --- Reactive processes
  // Resize
  $: {
    console.log('pixi layer resize');
    resizeApplication($width);
  }

  // --- Functions

  function resizeApplication(w) {
    if (w > 0) {
      console.log('resize pixi', w, initialHeight);

      const c = viewport.center;
      app.renderer.resize(w, initialHeight);
      app.renderer.view.style.width = `${w}px`;
      app.renderer.view.style.height = `${initialHeight}px`;
      viewport.resize(w, initialHeight, worldWidth, worldHeight);
      viewport.center = c;

      if (element) {
        requestRender();
      }
    }
  }

  function requestRender() {
    if (renderId) {
      return;
    }
    renderId = requestAnimationFrame(() => {
      app.render();
      renderId = null;
    });
  }

  function renderAnimation() {
    if (viewport.dirty) {
      requestRender();
      viewport.dirty = false;
    }
  }
</script>

<div
  bind:clientWidth={$width}
  bind:this={element}
  id="pixi-base"
  style="height: {initialHeight}px;">
  {#if $featureMode === false}
    <PixiLasso
      dataKey={dataKey}
      encodingKey={encodingKey}
      renderKey={renderKey} />
  {/if}
  <EdgesLayer
    dataKey={dataKey}
    encodingKey={encodingKey}
    renderKey={renderKey} />
  <NodesLayer
    dataKey={dataKey}
    encodingKey={encodingKey}
    renderKey={renderKey} />
  <ProgressBar
    encodingKey={encodingKey}
    renderKey={renderKey}
    initialWidth={initialWidth} />
  <LegendsLayer
    edgeMappingKey={edgeMappingKey}
    nodeMappingKey={nodeMappingKey}
    renderKey={renderKey} />
</div>

<style>
  #pixi-base {
    width: 100%;
  }
</style>
