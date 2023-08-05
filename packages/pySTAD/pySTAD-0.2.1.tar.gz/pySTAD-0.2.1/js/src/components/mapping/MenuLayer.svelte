<script>
  import { crossfade, scale } from 'svelte/transition';
  import nodeIcon from '../../assets/images/node.png';
  import edgeIcon from '../../assets/images/edge.png';
  import layoutIcon from '../../assets/images/layout.png';
  import NodeMapping from './NodeMapping.svelte';
  import EdgeMapping from './EdgeMapping.svelte';
  import LayoutSimulation from './LayoutSimulation.svelte';

  // --- Component props
  export let dataKey = null;
  export let encodingKey = null;
  export let nodeMappingKey = null;
  export let edgeMappingKey = null;

  // --- Menu state
  let visible = ''; // can be set to: '', 'node', 'edge', 'layout'.

  const [send, receive] = crossfade({
    duration: 200,
    fallback: scale
  });
</script>

<NodeMapping
  bind:visible
  dataKey={dataKey}
  encodingKey={encodingKey}
  nodeMappingKey={nodeMappingKey}
  receive={receive}
  send={send} />
<EdgeMapping
  bind:visible
  dataKey={dataKey}
  edgeMappingKey={edgeMappingKey}
  encodingKey={encodingKey}
  receive={receive}
  send={send} />
<LayoutSimulation
  bind:visible
  dataKey={dataKey}
  encodingKey={encodingKey}
  receive={receive}
  send={send} />

{#if visible === ''}
  <div id="menu-container">
    <button
      id="node-button"
      in:receive={{ key: 'node' }}
      out:send={{ key: 'node' }}
      on:click={() => (visible = 'node')}>
      <img src={nodeIcon} alt="A node icon." />
    </button>
    <button
      id="edge-button"
      in:receive={{ key: 'edge' }}
      out:send={{ key: 'edge' }}
      on:click={() => (visible = 'edge')}>
      <img src={edgeIcon} alt="An edge icon." />
    </button>
    <button
      id="layout-button"
      in:receive={{ key: 'layout' }}
      out:send={{ key: 'layout' }}
      on:click={() => (visible = 'layout')}>
      <img src={layoutIcon} alt="A layout icon." />
    </button>
  </div>
{/if}

<style>
  #menu-container {
    display: flex;
    flex-direction: column;
    width: 30px;
    height: 100px;
    position: absolute;
    top: 10px;
    left: 10px;
  }

  button {
    width: 30px;
    height: 30px;
    margin: 1px;
    padding: 1px;
    border-width: 2px;
    border-color: rgb(118, 118, 188);
  }

  button img {
    width: 100%;
    height: 100%;
  }
</style>
