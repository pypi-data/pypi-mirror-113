// Adapted from
// - https://observablehq.com/@fil/worker

export function worker(worker, callback) {
  worker.onmessage = (r) => callback(r.data);

  function updater(args, transferList) {
    worker.postMessage(args, transferList);
  }

  updater.destroy = function () {
    worker.terminate();
  };

  return updater;
}
