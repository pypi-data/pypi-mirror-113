<script>
  import { getContext } from 'svelte';
  import { Graphics } from 'pixi.js';

  // --- Component properties
  export let dataKey = null;
  export let encodingKey = null;
  export let renderKey = null;

  // --- Context
  const { nodes, edges } = getContext(dataKey);
  const { nodePositions, progress, edgeColors, edgeWidths, edgeAlpha } =
    getContext(encodingKey);
  const { viewport, requestRender } = getContext(renderKey);

  // --- Graphics objects
  const edgeLayer = new Graphics();
  viewport.addChild(edgeLayer);

  // --- Reactive processes
  $: if ($progress === 0) {
    edgeLayer.alpha = $edgeAlpha;
    updateEdges($edgeColors, $edgeWidths);
  }

  $: if ($progress === 1) {
    clearEdges();
  }

  // --- Functions
  function updateEdges(colors_, widths_) {
    if (
      !colors_ ||
      !widths_ ||
      $nodePositions.length !== $nodes.length ||
      $nodes.length === 0
    ) {
      console.log('abort edge update');
      return;
    }
    edgeLayer.clear();
    $edges.forEach((e, idx) => {
      const sourcePosition = $nodePositions[e.source];
      const targetPosition = $nodePositions[e.target];
      edgeLayer
        .lineStyle(widths_[idx], colors_[idx])
        .moveTo(sourcePosition.x, sourcePosition.y)
        .lineTo(targetPosition.x, targetPosition.y);
    });

    requestRender();
  }

  function clearEdges() {
    edgeLayer.clear();
  requestRender();
  }
</script>
