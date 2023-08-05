import {
  forceManyBody,
  forceLink,
  forceSimulation,
  forceCenter
} from 'd3-force';

// State
let nodes = null;
let links = null;
let linksWaiting = false;
let baseRepulsion = 0;
let repulsionPower = 0;
let repulsionNormalisation = 1;

let totalIterations = 0;
let iteration = 0;

// Simulation
const repulsionForce = forceManyBody();
const linkForce = forceLink();
const centerForce = forceCenter();
// The simulation stops automatically when minAlpha is reached.
const layoutSim = forceSimulation()
  .force('center', forceCenter())
  .force('charge', repulsionForce)
  .force('link', linkForce)
  .force('center', centerForce)
  .stop()
  .on('tick', () => {
    self.postMessage({
      progress: iteration <= 1 ? 0 : iteration / totalIterations,
      positions: nodes.map((n) => {
        return { x: n.x, y: n.y };
      })
    });
    --iteration;
  });

function updateNodes(messageNodes) {
  if (!nodes || nodes.length !== messageNodes.length) {
    nodes = messageNodes.map((r, idx) => {
      return { id: idx, r: r };
    });
    layoutSim.nodes(nodes);
    if (linksWaiting) {
      linkForce.links(links);
      linksWaiting = false;
    }
    repulsionNormalisation = Math.pow(nodes.length, repulsionPower);
    repulsionForce.strength(-baseRepulsion / repulsionNormalisation);
  } else {
    messageNodes.forEach((r, idx) => {
      nodes[idx].r = r;
    });
  }
}

function updateLinks(messageLinks) {
  if (!links || links.length !== messageLinks.length) {
    links = messageLinks;
    if (nodes) {
      linkForce.links(links);
    } else {
      linksWaiting = true;
    }
  }
}

function updateProps(props) {
  baseRepulsion = props.simulation_repulsion_strength;
  repulsionPower = props.simulation_repulsion_normalization;
  repulsionNormalisation = nodes ? Math.pow(nodes.length, repulsionPower) : 1;
  repulsionForce.strength(-baseRepulsion / repulsionNormalisation);
  linkForce.strength((l) => props.simulation_link_strength * l.distance);
  centerForce.strength(props.simulation_center_strength);
  repulsionForce.distanceMax(props.simulation_repulsion_limit);
}

function dragNode({ idx, x, y }) {
  nodes[idx].fx = x;
  nodes[idx].fy = y;
}

function runSimulation(alpha) {
  // Set the specified alpha
  layoutSim.alpha(alpha);

  // Compute number of iterations
  const minAlpha = layoutSim.alphaMin();
  const decay = layoutSim.alphaDecay();
  const newIterations = Math.round(
    Math.log(minAlpha / alpha) / Math.log(1 - decay)
  );
  totalIterations = Math.max(iteration, newIterations);
  iteration = totalIterations;
  layoutSim.restart();
}

function workerMain(message) {
  if (message.updateNodes) {
    if (message.nodes.length > 0) {
      updateNodes(message.nodes);
    }
  }
  if (message.updateLinks) {
    if (message.links.length) {
      updateLinks(message.links);
    }
  }
  if (message.updateProps) {
    updateProps(message.props);
  }
  if (message.updateDrag) {
    dragNode(message.node);
  }

  if (nodes && links) {
    runSimulation(message.alpha);
  }
}

self.onmessage = (e) => {
  workerMain(e.data);
};
