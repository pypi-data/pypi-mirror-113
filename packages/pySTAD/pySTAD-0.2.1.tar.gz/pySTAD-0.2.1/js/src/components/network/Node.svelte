<script>
  import { createEventDispatcher, getContext, onDestroy } from 'svelte';
  import { Circle, Container, Graphics } from 'pixi.js';

  // --- Component properties
  export let id = null;
  export let dataKey = null;
  export let renderKey = null;
  export let encodingKey = null;
  export let nodesLayerKey = null;
  export let stroke = 0xacacac;
  export let hoverStroke = 0x000000;
  export let strokeWidth = 0.1;
  export let notSelectedColor = 0xccd7d7;

  const dispatch = createEventDispatcher();

  // --- Context
  const { selectedNodes } = getContext(dataKey);
  const { nodePositions, nodeColors, nodeRadii, moveNode } =
    getContext(encodingKey);
  const { app, viewport, requestRender } = getContext(renderKey);
  const { nodesLayer, frontLayer, nodesMap } = getContext(nodesLayerKey);

  // --- Graphics objects
  const border = new Graphics();
  const circle = new Graphics();
  const nodeGfx = new Container();

  // node properties
  nodeGfx.interactive = true;
  nodeGfx.buttonMode = true;
  nodeGfx.hitArea = new Circle();
  nodeGfx.position.set(0, 0);

  // interactions
  nodeGfx.on('mouseover', handleHoverStart);
  nodeGfx.on('mouseout', handleHoverEnd);
  nodeGfx.on('mousedown', handleDragStart);
  nodeGfx.on('mouseup', handleDragEnd);
  nodeGfx.on('mouseupoutside', handleDragEnd);

  // add node as children
  nodeGfx.addChild(circle);
  nodeGfx.addChild(border);
  nodesLayer.addChild(nodeGfx);
  nodesMap[id] = nodeGfx;

  onDestroy(() => {
    nodesLayer.removeChild(nodeGfx);
    frontLayer.removeChild(nodeGfx);
    delete nodesMap[id];
    nodeGfx.destroy(true);
  });

  // --- Reactive processes
  $: pos = $nodePositions[id];
  $: {
    // Only triggered when pos actually changes value!
    updatePosition(pos);
  }

  $: isSelected = $selectedNodes.length === 0 || $selectedNodes.includes(id);
  $: col = isSelected ? $nodeColors[id] : notSelectedColor;
  $: rad = $nodeRadii[id];
  $: {
    // Only triggered when col or rad actually changed value!
    updateVisuals(col, rad);
  }

  // --- Functions
  function updatePosition(pos) {
    if (!pos) {
      return;
    }

    nodeGfx.position.set(pos.x, pos.y);
    requestRender();
  }

  function updateVisuals(c, r) {
    if (!c || !r) {
      return;
    }

    nodeGfx.hitArea.radius = r + strokeWidth;
    circle
      .clear()
      .beginFill(c)
      .drawCircle(0, 0, r)
      .endFill(c)
      .lineStyle(strokeWidth, stroke)
      .drawCircle(0, 0, r);
    border.clear().lineStyle(strokeWidth, stroke).drawCircle(0, 0, r);
    requestRender();
  }

  function handleHoverStart() {
    border.tint = hoverStroke;
    dispatch('hoverStart', { id: id });
  }

  function handleHoverEnd() {
    border.tint = stroke;
    dispatch('hoverEnd', { id });
  }

  // eslint-disable-next-line no-unused-vars
  function handleDragStart(_) {
    app.renderer.plugins.interaction.on('mousemove', handleDragMove);
    viewport.pause = true;
    // dispatch('nodeClick', {id: id});
  }

  // eslint-disable-next-line no-unused-vars
  function handleDragEnd(_) {
    app.renderer.plugins.interaction.off('mousemove', handleDragMove);
    viewport.pause = false;
    handleDragMove(null); // tell the layout simulation to release the node
    // dispatch('nodeUnclick', {id: id});
  }

  function handleDragMove(event) {
    let x = null;
    let y = null;
    if (event) {
      const p = viewport.toWorld(event.data.global);
      x = p.x;
      y = p.y;
    }
    $moveNode({ id, x, y });
  }
</script>
