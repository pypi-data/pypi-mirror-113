const path = require('path');

const rules = [
    {
        test: /\.svelte$/,
        loader: 'svelte-loader'
    },
    { test: /\.worker\.(c|m)?js$/i, use: [
        {
          loader: 'worker-loader',
          options: {
            filename: '[name].worker.js',
            inline: 'fallback'
          },
        }
      ],
  },
    { test: /\.ts$/, loader: 'ts-loader' },
    { test: /\.js$/, loader: 'source-map-loader' },
    { test: /\.css$/, use: ['style-loader', 'css-loader']},
    { test: /\.(jpg|png)$/, loader: 'url-loader' }
];
const externals = ['@jupyter-widgets/base'];
const resolve = {
    alias: {
        svelte: path.resolve('node_modules', 'svelte')
    },
    extensions: ['.webpack.js', '.web.js', '.mjs', '.ts', '.js', '.svelte'],
    mainFields: ['svelte', 'browser', 'module', 'main'],
};
  
module.exports = (env, argv) => {
    var devtool = argv.mode === 'development' ? 'source-map' : false;
    return [
        { // Jupyter lab bundle
            mode: argv.mode,
            entry: {
                plugin: './src/plugin.ts',
            },
            output: {
                filename: '[name].js',
                path: path.resolve(__dirname, 'lib'),
                libraryTarget: 'amd',
            },
            module: {
                rules: rules,
            },
            devtool: devtool,
            externals,
            resolve,
        }
    ];
}
