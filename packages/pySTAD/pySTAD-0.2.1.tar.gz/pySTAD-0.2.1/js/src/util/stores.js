import { writable, readable } from 'svelte/store';

export function createWritableValue(model, name_) {
  const name = name_;
  const curVal = writable(model.get(name));

  model.on('change:' + name, () => curVal.set(model.get(name)), null);

  return {
    set: (v) => {
      curVal.set(v);
      model.set(name, v);
      model.save_changes();
    },
    subscribe: curVal.subscribe,
    update: (func) => {
      curVal.update((v) => {
        const out = func(v);
        model.set(name, out);
        model.save_changes();
        return out;
      });
    }
  };
}

export function createReadableValue(model, name_) {
  const name = name_;
  return readable(model.get(name), (set) => {
    model.on('change:' + name, () => set(model.get(name)), null);
    return () => {};
  });
}
