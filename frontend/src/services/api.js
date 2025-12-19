import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const cpfService = {
  consultar: async (cpf) => {
    const response = await axios.post(`${API}/cpf/consultar`, { cpf });
    return response.data;
  }
};

export const darfService = {
  obter: async (protocol) => {
    const response = await axios.get(`${API}/darf/${protocol}`);
    return response.data;
  }
};

export const pixService = {
  gerar: async (protocol, value, cpf, nome = '') => {
    const response = await axios.post(`${API}/pix/gerar`, { protocol, value, cpf, nome });
    return response.data;
  },
  verificar: async (protocol) => {
    const response = await axios.get(`${API}/pix/verificar/${protocol}`);
    return response.data;
  }
};