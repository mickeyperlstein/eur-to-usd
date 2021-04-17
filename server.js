const http = require('http')
const server = http.createServer((req, res) => {
    console.log('New connection')
    res.end('Hello Awsome eur-to-usd v2')
})

const PORT = process.env.PORT || 8080
server.listen(PORT, ()=> console.log('Listenning on port ' + PORT) )
