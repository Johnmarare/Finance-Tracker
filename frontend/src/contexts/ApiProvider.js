import React, { createContext, useContext } from 'react';
import FedhaApiClient from '../FedhaApiClient';

const ApiContext = createContext();

export default function ApiProvider({ children }) {
    const api = new FedhaApiClient();
  
    return (
      <ApiContext.Provider value={api}>
        {children}
      </ApiContext.Provider>
    );
  }
  
  export function useApi() {
    return useContext(ApiContext);
  }