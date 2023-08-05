<script>
  import { setContext } from 'svelte';
  import { derived, writable } from 'svelte/store';
  import { createReadableValue, createWritableValue } from './util/stores';
  import NeighbourMap from './components/NeighbourMap.svelte';
  import EncodingLayer from './components/EncodingLayer.svelte';

  // --- Component properties
  export let model;

  // --- Global context
  const dataKey = {};
  // The current communication-schema between server and client does not consider
  // partial updates to the network. All aspects of the network are updated in the
  // client, even when only (f.i.) the node-color data changed...
  const network = createReadableValue(model, 'network');
  const featureMode = createReadableValue(model, 'featureMode');
  const selectedNodes = createWritableValue(model, 'selectedNodes');

  setContext(dataKey, {
    nodes: derived(network, () => $network[0]),
    edges: derived(network, () => $network[1]),
    selectedNodes: selectedNodes,
    featureMode: featureMode,
    neighbours: writable({})
  });
</script>

<div id="stad-widget-main">
  <EncodingLayer dataKey={dataKey} />
  <NeighbourMap dataKey={dataKey} />
</div>
<br />

<style>
  #stad-widget-main {
    width: 100%;
    margin: 5px;
  }
</style>