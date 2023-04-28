const { app, BrowserWindow } = require('electron');

let win;

// var child = require('child_process').execFile;
// var executablePath = 'dist/main.exe';

// child(executablePath, function (err, data) {
//   if (err) {
//     console.error(err);
//     return;
//   }

//   // createWindow();
// });

function createWindow() {
  win = new BrowserWindow({
    width: 920,
    height: 580,
    center: true,
    minWidth: 700,
    minHeight: 540,
    icon: __dirname + '/img/icon2.png',
    autoHideMenuBar: true,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      // preload: path.join(__dirname, 'preload.js'),
    },
  });

  win.loadFile('index.html');

  // win.webContents.openDevTools();

  win.on('closed', () => {
    win = null;
  });
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
  app.quit();
});

// to_csv(someData);
