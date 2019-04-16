const merge = require('webpack-merge');
const common = require('./webpack.common.js');

module.exports = merge(common, {
  mode: 'production',
  devtool: 'source-map',
  externals: {
    // global app config object
    config: JSON.stringify({
      apiUrl: 'http://localhost:8080'
    })
  }
});
