import React, { useState, useEffect } from "react";
import HomeContainer from "../../components/home/HomeContainer";

const HomePage = () => {
  const [data, setData] = useState();
  const queryString = window.location.search
  const params = new URLSearchParams(queryString);
  useEffect(() => {
    fetch("/suppliers/"+params.get('supplier'))
      .then((res) => res.json())
      .then((data) => {
        setData(JSON.parse(data.data));
      });
  }, []);
  console.log(params.get('supplier'));
  return <HomeContainer paketo={data} />;
};

export default HomePage;
