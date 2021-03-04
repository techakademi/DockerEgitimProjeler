const express = require('express');
const bodyParser = require('body-parser');
const request = require('request');
const app = express()
const PORT = process.env.PORT || 3000;

const apiKey = '9035a32a7a94948c873b371808f80a7f';

app.use(express.static('public'));
app.use(bodyParser.urlencoded({ extended: true }));
app.set('view engine', 'ejs')

app.get('/', function (req, res) {
  res.render('index', {weather: null, error: null});
})

app.post('/', function (req, res) {
  let city = req.body.city;
  let url = `http://api.openweathermap.org/data/2.5/weather?q=${city}&units=metric&appid=${apiKey}&lang=tr`

  request(url, function (err, response, body) {
    if(err){
      res.render('index', {weather: null, error: 'Hata !, Lütfen Tekrar Deneyin'});
    } else {
      let weather = JSON.parse(body)
      if(weather == undefined ){
        res.render('index', {weather: null, error: 'Hata !, Lütfen Tekrar Deneyin'});
      } else {
        let weatherText = `Hava sıcaklığı ${weather.name}'da şu an ${weather.main.temp} derece ! /  hissedilen ise (${weather.main.feels_like}) / Nem oranı:(%${weather.main.humidity}) / Rüzgar hızı ${weather.wind.speed}`;
        res.render('index', {weather: weatherText, error: null});
      }
    }
  })
})

app.listen(PORT, () => {
  console.log(`Bu uygulama ${ PORT } nolu portu dinliyor !!!`);
});