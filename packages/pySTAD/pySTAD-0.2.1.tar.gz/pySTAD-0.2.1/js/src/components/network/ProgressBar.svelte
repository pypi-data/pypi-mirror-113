<script>
  import { getContext } from 'svelte';
  import { Graphics } from 'pixi.js';
  import { scaleLinear } from 'd3-scale';

  // --- Component properties
  export let renderKey = null;
  export let encodingKey = null;
  export let initialWidth = 0;
  export let progressColor = 0x1b83e9;

  // --- Context
  const { progress } = getContext(encodingKey);
  const { app, width, requestRender } = getContext(renderKey);

  // --- Graphics objects
  const progressGraphic = new Graphics();
  const progressScale = scaleLinear().domain([1, 0]).range([0, initialWidth]);

  app.stage.addChild(progressGraphic);

  // --- Reactive processes
  $: if ($width > 0) {
    progressScale.range([0, $width]);
  }

  $: {
    progressGraphic.clear();
    if ($progress > 0) {
      progressGraphic
        .beginFill(progressColor)
        .drawRect(0, 0, progressScale($progress), 2)
        .endFill();
    }
    requestRender();
  }
</script>
