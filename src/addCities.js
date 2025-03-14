import fs from 'fs';  // Importa o módulo fs
import db from './firebase.js';  // Importa a configuração do Firebase
import { collection, doc, setDoc } from 'firebase/firestore';  // Importa as funções do Firestore

const addCities = async () => {
  // Lê o arquivo JSON de forma assíncrona
  const cidades = JSON.parse(await fs.promises.readFile('./cidades.json', 'utf-8'));

  // Adiciona as cidades no Firestore
  for (const [city, connections] of Object.entries(cidades)) {
    const cityRef = doc(collection(db, 'cities'), city);  // Criando referência para o documento
    await setDoc(cityRef, connections);  // Adicionando os dados no Firestore
  }
};

addCities();  // Executa a função para adicionar as cidades
