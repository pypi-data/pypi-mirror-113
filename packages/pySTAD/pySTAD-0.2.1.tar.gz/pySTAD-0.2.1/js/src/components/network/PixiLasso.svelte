<script>
  import { getContext } from 'svelte';
  import { Graphics } from 'pixi.js';
  import classifyPoint from 'robust-point-in-polygon';
  import { pixiKey } from '../../util/PixiKeyboard.js';

  // --- Component properties
  export let dataKey = null;
  export let encodingKey = null;
  export let renderKey = null;
  export let triggerKey = 'Control';
  export let alpha = 0.2;
  export let color = 0xa7a7a7;
  export let closingThreshold = 100;

  // --- Selection variables
  let selectionOrigin = null;
  let selectionEnd = null;
  let selectionPath = [];

  // --- Context variables
  const { app, viewport, requestRender } = getContext(renderKey);
  const { nodePositions } = getContext(encodingKey);
  const { selectedNodes } = getContext(dataKey);

  // --- Graphics and interaction
  const selectionGraphic = new Graphics();
  selectionGraphic.alpha = alpha;
  viewport.addChild(selectionGraphic);

  const selectionKey = pixiKey(triggerKey);
  selectionKey.press = enableSelection;
  selectionKey.release = disableSelection;

  // --- Functions
  function enableSelection() {
    app.renderer.plugins.interaction.on('mousedown', startSelection);
    app.renderer.plugins.interaction.on('mouseup', endSelection);
    viewport.pause = true;
  }

  function disableSelection() {
    app.renderer.plugins.interaction.off('mousedown', startSelection);
    if (selectionPath.length === 0) {
      app.renderer.plugins.interaction.off('mouseup', endSelection);
    }
    viewport.pause = false;
  }

  function startSelection(e) {
    // Reset selection path and origin
    const point = e.data.global;
    selectionPath = [viewport.toWorld(point)];
    selectionOrigin = [point.x, point.y];

    // Reset selected nodes
    $selectedNodes = [];

    // Engage selection update
    app.renderer.plugins.interaction.on('mousemove', updateSelection);
  }

  function updateSelection(e) {
    const point = e.data.global;
    selectionPath.push(viewport.toWorld(point));
    selectionEnd = [point.x, point.y];

    selectionGraphic
      .clear()
      .beginFill(color)
      .drawPolygon(selectionPath)
      .endFill();

    requestRender();
  }

  // eslint-disable-next-line no-unused-vars
  function endSelection(_) {
    app.renderer.plugins.interaction.off('mousemove', updateSelection);
    if (selectionKey.isUp) {
      app.renderer.plugins.interaction.off('mouseup', endSelection);
    }

    // Remove selection rectangle
    selectionGraphic.clear();

    // Check closing conditions
    const distance = Math.sqrt(
      Math.pow(selectionOrigin[0] - selectionEnd[0], 2) +
        Math.pow(selectionOrigin[1] - selectionEnd[1], 2)
    );

    if (selectionPath.length <= 2 || distance > closingThreshold) {
      requestRender();
      return;
    }

    // Find nodes within selection
    const path = selectionPath.map((p) => [p.x, p.y]);
    selectionPath = []; // disables end-selection callback when key is released
    $selectedNodes = $nodePositions.reduce((acc, p, idx) => {
      if (classifyPoint(path, [p.x, p.y]) < 0) {
        acc.push(idx);
      }
      return acc;
    }, []);
  }
</script>
