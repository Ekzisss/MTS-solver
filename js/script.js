const fs = require('fs');
const { getJSON } = require('jquery');
const path = require('path');

$('.loading').show();
$(document).ready(function () {
  errors = fs.readFileSync('error.json', 'utf8');

  const obj = JSON.parse(fs.readFileSync('data.json', 'utf8'));
  const inputs = document.querySelectorAll('.data-enter__input');

  Array.from(obj).map((val, index) => {
    // console.log(val);
    // console.log(index);
    inputs[index].setAttribute('placeholder', val);
  });

  if (errors) {
    $('.data-enter__title').after(
      '<div class="error">Ошибка входных данных</div>'
    );
    $('.loading').hide();
  } else {
    var child = require('child_process').execFile;
    var executablePath = path.join(__dirname, 'dist/main/main.exe');

    child(executablePath, function (err, data) {
      if (err) {
        console.error(err);
        return;
      }

      $('.loading').hide();

      $('#heatmap').append(
        '<img src="img/heatmap.png" alt="heatmap" class="heatmap__img" />'
      );

      $('#heatmap2').append(
        '<img src="img/heatmap2.png" alt="heatmap rk" class="heatmap__img" />'
      );

      $('#heatmap3').append(
        '<img src="img/heatmap3.png" alt="heatmap fi" class="heatmap__img" />'
      );

      $('.graph').append(
        '<img src="img/graphs.png" alt="graph" class="graph__img" />'
      );
      return;
    });
  }

  $('.menu__item').click(function (e) {
    e.preventDefault();
    switch (e.target.id) {
      case '1':
        $('main').hide();
        $('.data-enter').show();
        $('.menu__item').removeClass('menu__item--active');
        $(e.target).addClass('menu__item--active');
        break;
      case '2':
        $('main').hide();
        $('#heatmap').show();
        $('.menu__item').removeClass('menu__item--active');
        $(e.target).addClass('menu__item--active');
        break;
      case '3':
        $('main').hide();
        $('#heatmap2').show();
        $('.menu__item').removeClass('menu__item--active');
        $(e.target).addClass('menu__item--active');
        break;
      case '4':
        $('main').hide();
        $('#heatmap3').show();
        $('.menu__item').removeClass('menu__item--active');
        $(e.target).addClass('menu__item--active');
        break;
      case '5':
        $('main').hide();
        $('.graph').show();
        $('.menu__item').removeClass('menu__item--active');
        $(e.target).addClass('menu__item--active');
        break;
      case '6':
        $('main').hide();
        $('.discription').show();
        $('.menu__item').removeClass('menu__item--active');
        $(e.target).addClass('menu__item--active');
        break;
      case '7':
        $('main').hide();
        $('.About').show();
        $('.menu__item').removeClass('menu__item--active');
        $(e.target).addClass('menu__item--active');
        break;
      default:
        console.log('error');
        break;
    }
  });

  $('.data-enter__save').click(function (e) {
    e.preventDefault();
    data = $('.data-enter__input');
    file = [];
    $.map(data, function (elem, index) {
      val = $(elem).val();
      console.log(typeof val);
      if (val == '') {
        file.push($(elem).attr('placeholder'));
      } else {
        file.push(val);
      }
    });

    file.forEach((element) => {
      element = parseFloat(element);
      // console.log(element);
      if (isNaN(element) || parseFloat(element) <= 0) {
        er = {
          error: 'error',
        };
        // console.log(er);
        fs.writeFileSync('error.json', JSON.stringify(er));
      }
      fs.writeFileSync('data.json', JSON.stringify(file));
      window.location = '';
    });

    // console.log(typeof er !== 'undefined');
    // console.log(typeof er);

    if (typeof er !== 'undefined') {
      window.location = '';
      return;
    } else {
      // console.log('123');

      file = JSON.stringify(file);

      fs.writeFileSync('error.json', '');
      fs.writeFileSync('data.json', file);

      window.location = '';
    }
  });

  $('.data-enter__reset').click(function (e) {
    e.preventDefault();

    fs.writeFileSync('error.json', '');

    file =
      '["100","300","500","500","500","15","15","22.5","22.5","0.001","2","20"]';

    fs.writeFileSync('data.json', file);
    window.location = '';
  });
});
