<script>
  import { getContext, onDestroy } from 'svelte';
  import { worker } from '../../util/worker.js';
  import Worker from '../../workers/layout.worker.js';

  // --- Component properties
  export let dataKey = null;
  export let encodingKey = null;
  export let visible = '';
  export let receive = null;
  export let send = null;

  // --- Contexts
  const { nodeRadii, nodePositions, progress, moveNode } =
    getContext(encodingKey);
  const { edges } = getContext(dataKey);
  $moveNode = dragNode;

  // --- Simulation variables
  const updateAlpha = 0.3;
  let run = true;

  let initialAlpha = 2;
  let centerStrength = 0.2;
  let linkStrength = 0.1;
  let linknormalization = 0.1;
  let repulsionStrength = 1;
  let repulsionNormalization = 0.1;
  let repulsionLimit = 150;
  let approximation = 0.7;

  // --- Webworker that runs layout simulation
  const simulation = worker(new Worker(), (message) => {
    $nodePositions = message.positions;
    $progress = message.progress;
  });

  // --- Lifetime
  onDestroy(() => {
    simulation.destroy();
  });

  // --- Reactive processes
  // Simulation properties
  $: {
    console.log('simulation settings changed');
    updateSimulationProperties(
      run,
      repulsionLimit,
      repulsionNormalization,
      repulsionStrength,
      linkStrength,
      centerStrength,
      initialAlpha,
      linknormalization
    );
  }

  // Nodes
  $: {
    updateNodes($nodeRadii);
  }

  // Edges
  $: {
    updateEdges($edges);
  }

  function updateSimulationProperties(
    run_,
    repulsionLimit_,
    repulsionNormalization_,
    repulsionStrength_,
    linkStrength_,
    centerStrength_,
    initialAlpha_,
    linknormalization_
  ) {
    if (run_) {
      simulation({
        updateNodes: false,
        updateLinks: false,
        updateProps: true,
        updateDrag: false,
        props: {
          simulation_link_strength: linkStrength_,
          simulation_center_strength: centerStrength_,
          simulation_repulsion_strength: repulsionStrength_,
          simulation_repulsion_limit: repulsionLimit_,
          simulation_repulsion_normalization: repulsionNormalization_,
          simulation_link_normalization: linknormalization_
        },
        alpha: initialAlpha_
      });
    }
  }

  function updatePositionAllocation(numNewNodes) {
    if (numNewNodes !== $nodePositions.length) {
      $nodePositions = Array.from({ length: numNewNodes }, () => {
        return {
          x: 0,
          y: 0
        };
      });
    }
  }

  function updateNodes(nodesRadii_) {
    console.log('nodes changed in layout simulation');
    // The layout simulation only needs to know the radius of each node.
    // So, the array of node radii contains all information, as the ID of each
    // node is encoded in the position of the value in the array.
    if (run) {
      simulation({
        updateNodes: true,
        updateLinks: false,
        updateProps: false,
        updateDrag: false,
        nodes: nodesRadii_,
        alpha: initialAlpha
      });
    } else {
      updatePositionAllocation(nodesRadii_.length);
    }
  }

  function updateEdges(edges_) {
    if (run) {
      console.log('edges changed in layout simulation');
      simulation({
        updateNodes: false,
        updateLinks: true,
        updateProps: false,
        updateDrag: false,
        links: edges_.map((e) => {
          return {
            source: e.source,
            target: e.target,
            distance: e.distance
          };
        }),
        alpha: initialAlpha
      });
    }
  }

  function dragNode(event) {
    const { id, x, y } = event;
    if (run) {
      simulation({
        updateDrag: true,
        updateNodes: false,
        updateLinks: false,
        updateProps: false,
        alpha: updateAlpha,
        node: {
          idx: id,
          x: x,
          y: y
        }
      });
    }
  }
</script>

{#if visible === 'layout'}
  <div
    id="simulation-container"
    in:receive={{ key: 'layout' }}
    out:send={{ key: 'layout' }}>
    <buttton id="close-button" on:click={() => (visible = '')}>
      <span>&times;</span>
    </buttton>
    <label>
      <input type="checkbox" bind:checked={run} />
      Run simulation
    </label>
    <label>
      Initial temperature
      <input
        type="range"
        bind:value={initialAlpha}
        min="0"
        max="5"
        step="0.1" />
    </label>
    <label>
      Link strength
      <input
        type="range"
        bind:value={linkStrength}
        min="0"
        max="2"
        step="0.01" />
    </label>
    <label>
      Link normalization
      <input
        type="range"
        bind:value={linknormalization}
        min="0"
        max="1"
        step="0.05" />
    </label>
    <label>
      Repulsion strength
      <input
        type="range"
        bind:value={repulsionStrength}
        min="0"
        max="30"
        step="0.1" />
    </label>
    <label>
      Repulsion normalization
      <input
        type="range"
        bind:value={repulsionNormalization}
        min="0"
        max="1"
        step="0.05" />
    </label>
    <label>
      Repulsion limit
      <input
        type="range"
        bind:value={repulsionLimit}
        min="0"
        max="1000"
        step="5" />
    </label>
    <label>
      Center strength
      <input
        type="range"
        bind:value={centerStrength}
        min="0"
        max="10"
        step="0.05" />
    </label>
    <label>
      Simulation accuracy
      <input
        type="range"
        bind:value={approximation}
        min="0"
        max="1"
        step="0.05" />
    </label>
  </div>
{/if}

<style>
  #simulation-container {
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

  input[type='range'] {
    width: calc(100% - 16px);
  }
</style>
