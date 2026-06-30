// ─────────────────────────────────────────────────────────────────────────
// TradeLine Marketplace — Shared Site Data
// US States, tradeline inventory, contact info, wallet display addresses
// ─────────────────────────────────────────────────────────────────────────

const US_STATES = [
  ["AL","Alabama"],["AK","Alaska"],["AZ","Arizona"],["AR","Arkansas"],["CA","California"],
  ["CO","Colorado"],["CT","Connecticut"],["DE","Delaware"],["FL","Florida"],["GA","Georgia"],
  ["HI","Hawaii"],["ID","Idaho"],["IL","Illinois"],["IN","Indiana"],["IA","Iowa"],
  ["KS","Kansas"],["KY","Kentucky"],["LA","Louisiana"],["ME","Maine"],["MD","Maryland"],
  ["MA","Massachusetts"],["MI","Michigan"],["MN","Minnesota"],["MS","Mississippi"],["MO","Missouri"],
  ["MT","Montana"],["NE","Nebraska"],["NV","Nevada"],["NH","New Hampshire"],["NJ","New Jersey"],
  ["NM","New Mexico"],["NY","New York"],["NC","North Carolina"],["ND","North Dakota"],["OH","Ohio"],
  ["OK","Oklahoma"],["OR","Oregon"],["PA","Pennsylvania"],["RI","Rhode Island"],["SC","South Carolina"],
  ["SD","South Dakota"],["TN","Tennessee"],["TX","Texas"],["UT","Utah"],["VT","Vermont"],
  ["VA","Virginia"],["WA","Washington"],["WV","West Virginia"],["WI","Wisconsin"],["WY","Wyoming"],
  ["DC","District of Columbia"]
];

function populateStateSelect(selectEl, placeholder) {
  if (!selectEl) return;
  selectEl.innerHTML = '<option value="">' + (placeholder || 'Select state') + '</option>' +
    US_STATES.map(s => `<option value="${s[0]}">${s[1]}</option>`).join('');
}

// Contact info
const SITE_CONTACT = {
  whatsapp: 'https://wa.me/12625837916',
  whatsappDisplay: '+1 (262) 583-7916',
  telegram: 'https://t.me/TradeIQ_Plug1',
  telegramDisplay: '@TradeIQ_Plug1',
  email: 'marketplacetradeline@gmail.com'
};

// Wallet addresses for display only (no live payment processing)
const WALLET_ADDRESSES = {
  usdt: {
    'TRC-20': 'TNFTorYbtRQuMEHnBtxKVJudt8FCNnDXxZ',
    'ERC-20': '0x030C80DCC078bfCA89Cd29522D3Ad6C6422989A4',
    'BEP-20': '0x6bEB869150621957108586099c1F12Aa6E841A23',
    'Solana': '9PGaMHfoExqn69yuwRBM5ZxiQeQtBexXHKAGMxTfU7DE'
  },
  btc: {
    'BEP-20': '0x6bEB869150621957108586099c1F12Aa6E841A23',
    'Bitcoin': '34VTQzfkTqDzQvuvKepuQZabAXQyjNoZvx',
    'RENEC': '2118THmsx9wnDQnAVZufHb3JAMuEUaaJA4trTtQcNTNX'
  },
  ltc: {
    'Litecoin': 'MMUseN9FzhdyrvqVgMhpfjh1pKEbxBWypS'
  }
};
