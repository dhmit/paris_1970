const baseConfig = require('./webpack.config');

baseConfig.output.publicPath = "http://localhost:3000/build/";
baseConfig.optimization.minimize = false;
baseConfig.devServer = {
    port: 3000,
    headers: {
        "Access-Control-Allow-Origin": "*"
    },
    compress: true,
    hot: true
};
baseConfig.devtool = 'eval-source-map';

module.exports = baseConfig;
