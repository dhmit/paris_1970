const path = require("path");
const BundleTracker = require("webpack-bundle-tracker");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const ESLintPlugin = require("eslint-webpack-plugin");
const TerserPlugin = require("terser-webpack-plugin");
const Dotenv = require('dotenv-webpack');

module.exports = {
    context: __dirname,
    entry: {
        index: "./frontend/index"
    },
    output: {
        path: path.resolve("./assets/bundles/"),
        publicPath: "/static/bundles/",
        filename: "[name].bundle.js"
    },
    plugins: [
        new BundleTracker({filename: "./webpack-stats.json"}),
        new MiniCssExtractPlugin({filename: "[name].bundle.css"}),
        new ESLintPlugin(),
        new Dotenv({
            path: './.env', // Path to .env file (this is the default)
            safe: true, // load .env.example (defaults to "false" which does not use dotenv-safe)
        })
    ],
    module: {
        rules: [
            // Allow SVGs to be imported either as an asset (to use in an img src, e.g.)
            // or via SVGR as a ready-to-use component.
            // See docs: https://react-svgr.com/docs/webpack/#use-svgr-and-asset-svg-in-the-same-project
            {
                test: /\.svg$/i,
                type: 'asset',
                resourceQuery: /url/, // *.svg?url
            },
            {
                test: /\.svg$/i,
                issuer: /\.[jt]sx?$/,
                resourceQuery: { not: [/url/] }, // exclude react component if *.svg?url
                use: ['@svgr/webpack'],
            },


            // Load fonts
            {
                test: /\.(woff|woff2|eot|ttf)$/,
                use: "url-loader"
            },

            // eslint-disable-next-line max-len
            {
                test: /\.(scss|css)$/,
                use: [MiniCssExtractPlugin.loader, "css-loader", "sass-loader"]
            },
            {
                test: /\.js|.jsx$/,
                exclude: /node_modules/,
                use: "babel-loader"
            },

            {
                test: /\.(png|jpe?g|gif)$/i,
                use: [{loader: "file-loader"}]
            },
            {
                test: /\.mp4$/,
                use: "file-loader?name=videos/[name].[ext]"
            },

        ]
    },
    resolve: {
      extensions: ['.js', '.jsx'],
    },
    optimization: {
        minimize: true,
        minimizer: [new TerserPlugin()]
    }
};
