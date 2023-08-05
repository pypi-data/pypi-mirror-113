function addConnection(map, source, target) {
  if (map.has(source)) {
    const connected_nodes = map.get(source);
    connected_nodes.push(target);
  } else {
    map.set(source, [target]);
  }
}

self.onmessage = (e) => {
  const linkData = e.data.edges;
  const nodesMap = new Map();
  console.log('compute neighbours');

  linkData.forEach((l) => {
    addConnection(nodesMap, l.source, l.target);
    addConnection(nodesMap, l.target, l.source);
  });

  self.postMessage({
    neighbours: nodesMap
  });
};
