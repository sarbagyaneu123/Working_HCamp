const { getDefaultConfig } = require('expo/metro-config');
const path = require('path');

const config = getDefaultConfig(__dirname);

config.resolver = {
  ...config.resolver,
  extraNodeModules: {
    // Force a single React copy
    react: path.resolve(__dirname, 'node_modules/react'),
    'react/jsx-runtime': path.resolve(__dirname, 'node_modules/react/jsx-runtime'),
  },
};

module.exports = config;
