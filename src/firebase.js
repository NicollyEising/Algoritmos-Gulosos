// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFirestore } from 'firebase/firestore'; // Firestore
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDRTJwIlHUtgpdotnpzV21GIIUzvJTvt_I",
  authDomain: "algoritmosgulosos.firebaseapp.com",
  projectId: "algoritmosgulosos",
  storageBucket: "algoritmosgulosos.firebasestorage.app",
  messagingSenderId: "124819477867",
  appId: "1:124819477867:web:7185817a9dacf0a6b8682e"
};


// Inicializa o Firebase
const app = initializeApp(firebaseConfig);

// Inicializa o Firestore
const db = getFirestore(app);

export default db;