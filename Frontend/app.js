const express = require("express");
const app = express();
const axios = require("axios");
require("dotenv").config();
// Imposto come percorso di base /public
app.use(express.static(__dirname + "/public"));

app.get("/", (req, res) => {
  //CARICO INDEX HTML ALL'URL PRINCIPALE DEL SITO
  // let register = await axios.get(
  //   `${process.env.API}checkLogin`,
  //   req.axiosHeader
  // );
  // register.length
  //   ? res.sendFile(__dirname + "/home.html")
  //   : res.sendFile(__dirname + "/index.html");

  res.sendFile(__dirname + "/index.html");
});

app.get("/login", async (req, res) => {
  try {
    res.redirect(`${process.env.API}login`);
  } catch (err) {
    res.status(500).send(err.toString());
  }
});

app.get("/home", async (req, res) => {
  try {
    res.sendFile(__dirname + "/home.html");
  } catch (err) {
    res.status(500).send(err.toString());
  }
});

app.get("/getDatiArtista/:artId", async (req, res) => {
  try {
    const result = await axios.get(
      `${process.env.API}artistid=${req.params.artId}`,
      req.axiosHeader
    );
    res.status(200).send(result.data);
  } catch (err) {
    res.status(500).send(err.toString());
  }
});

app.listen(process.env.PORT, () => {
  console.log(`Open the project too http://localhost:${process.env.PORT}`);
});
