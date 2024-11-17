ymaps.ready(init);

function init() {
  // Создаем карту
  const map = new ymaps.Map("map", {
    center: [55.751574, 37.573856], // Центр Москвы
    zoom: 10,
    controls: ["searchControl", "zoomControl"],
  });

  // Получаем доступ к строке поиска
  const searchControl = map.controls.get("searchControl");

  // Добавляем метку для выбора локации
  let placemark;

  // Обновление координат на карте
  function updateCoordinates(coords) {
    document.getElementById("coords").textContent = `${coords[0].toFixed(6)}, ${coords[1].toFixed(6)}`;

    document.getElementById("latitude").value = coords[0];
    document.getElementById("longitude").value = coords[1];

    if (placemark) {
      placemark.geometry.setCoordinates(coords);
    } else {
      placemark = new ymaps.Placemark(coords, {}, { draggable: true });
      map.geoObjects.add(placemark);

      // Обновляем координаты при перетаскивании метки
      placemark.events.add("dragend", function () {
        const newCoords = placemark.geometry.getCoordinates();
        updateCoordinates(newCoords);
      });
    }
  }

  // Добавляем обработчик клика на карту
  map.events.add("click", function (event) {
    const coords = event.get("coords");
    updateCoordinates(coords);
  });

  // Добавляем обработчик поиска
  searchControl.events.add("resultselect", function (event) {
    const index = event.get("index");
    searchControl.getResult(index).then(function (result) {
      const coords = result.geometry.getCoordinates();
      updateCoordinates(coords);
      map.setCenter(coords, 15); // Центруем карту
    });
  });
}
