module.exports = {
    css: {
      loaderOptions: {
        less: {
          lessOptions: {
            modifyVars: {
              'primary-color': '#ff0000',
              'link-color': '#ffff00',
              'border-radius-base': '2px',
            },
            javascriptEnabled: true,
          },
        },
      },
    },
  };