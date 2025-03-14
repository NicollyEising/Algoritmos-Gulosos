const getCityConnections = async (cityName) => {
    const cityRef = db.collection('cities').doc(cityName);
    const doc = await cityRef.get();
    if (doc.exists) {
      console.log('Connections: ', doc.data());
    } else {
      console.log('No such city!');
    }
  };
  
  getCityConnections('Abdon Batista');
  