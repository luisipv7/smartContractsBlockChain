module.exports = {
  networks: {
    development: {
      host: "127.0.0.1",     // Localhost (default: none)
      port: 8545,            // Padrão: 8545
      network_id: "*",       // Qualquer rede (default: none)
    },
  },

  // Configurações adicionais...
  compilers: {
    solc: {
      version: "0.8.0",    // Defina a versão do compilador Solidity (opcional)
    },
  },
};
