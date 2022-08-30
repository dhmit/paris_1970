const path = require("path");
const BundleTracker = require("webpack-bundle-tracker");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const ESLintPlugin = require("eslint-webpack-plugin");
const TerserPlugin = require("terser-webpack-plugin");

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
        new ESLintPlugin()
    ],
    module: {
        rules: [
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

            {
                test: /\.svg$/i,
                issuer: /\.[jt]sx?$/,
                use: ["@svgr/webpack"]
            },
            {
                test: /\.(woff|woff2|eot|ttf)$/,
                use: "url-loader"
            }
        ]
    },
    optimization: {
        minimize: true,
        minimizer: [new TerserPlugin()]
    }
};
