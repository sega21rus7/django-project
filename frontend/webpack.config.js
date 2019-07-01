const path = require('path')
const webpack = require('webpack')
const {VueLoaderPlugin} = require('vue-loader')

module.exports = {
  mode: 'development',
  entry: path.resolve(__dirname, 'src/main'),
  module: {
    rules: [
      {test: /\.js$/, use: 'babel-loader'},
      {test: /\.vue$/, use: 'vue-loader'},
      {test: /\.css$/, use: ['vue-style-loader', 'css-loader']}
    ]
  },
  output: {
    path: path.resolve(__dirname, 'static'),
    publicPath: '/static/',
    filename: 'chat/main.js'
  },
  module: {
    rules: [{
      test: /\.vue$/,
      loader: 'vue-loader',
      options: {
        compilerOptions: {preserveWhitespace: false},
        hotReload: true,
        productionMode: false
      }
    }, {
      test: /\.s?css$/,
      use: [
        'vue-style-loader',
        {loader: 'css-loader', options: {importLoaders: 1}},
        'postcss-loader'
      ]
    }, {
      test: /\.pug$/,
      loader: 'pug-plain-loader'
    }, {
      test: /\.js$/,
      loader: 'babel-loader',
      include: [
        path.resolve(__dirname, 'src'),
        path.resolve(__dirname, 'node_modules')
      ],
      options: {
        cacheDirectory: false
      }
    }, {
      test: /\.(png|jpg|jpeg|gif|svg|woff|woff2|ttf|eot)$/,
      loader: 'file-loader',
      options: {
        name: 'frontend/files/[name].[hash:8].[ext]'
      }
    }
    ]
  },
  resolve: {
    modules: [
      path.resolve(__dirname, 'src'),
      path.resolve(__dirname, 'node_modules')
    ],
    alias: {
      'vue$': 'vue/dist/vue.esm.js'
    },
    extensions: ['.js', '.vue', '.css']
  },
  plugins: [
    new webpack.DefinePlugin({
      'process.env': {
        WEBPACK_PUBLIC_PATH: '\'/static/\''
      }
    }),
    new webpack.ProvidePlugin({
      _: 'lodash',
      axios: 'axios'
    }),
    new VueLoaderPlugin()
  ],
  devServer: {
    host: '0.0.0.0',
    port: 3030,
    inline: true,
    hot: true,
    overlay: {
      warnings: false,
      errors: true
    },
    proxy: [{
      context: () => true,
      target: `http://localhost:8008`
    }]
  },
  watchOptions: {poll: 1000}
}
