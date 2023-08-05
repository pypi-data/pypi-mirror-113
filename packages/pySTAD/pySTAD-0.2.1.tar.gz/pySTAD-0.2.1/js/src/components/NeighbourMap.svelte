<script>
  // TODO: move this functionality to the server side?
  import { getContext, onDestroy } from 'svelte';
  import { worker } from '../util/worker.js';
  import Worker from '../workers/neighbour.worker.js';

  // --- Component properties
  export let dataKey = null;

  // --- Global visualization context
  const { edges, neighbours } = getContext(dataKey);

  // --- Webworker (computes neighbour map: { id: [neibhours...] })
  const detectNeighbours = worker(new Worker(), (message) => {
    $neighbours = message.neighbours;
  });

  // --- Lifetime
  onDestroy(() => {
    detectNeighbours.destroy();
  });

  // --- Reactive processes
  // Edges changed, so recompute neighbours.
  $: {
    // Prevent errors due to hovering after edges changed but before the
    // updated neighbour map becomes available.
    $neighbours = null;
    detectNeighbours({ edges: $edges });
  }
</script>
