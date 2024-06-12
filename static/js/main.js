var map;
var circle;
var marker;
var facilityMarkers = [];
var clickedMarker;

function selectMapList() {
  if (map) {
    map.destroy();
  }
  map = new naver.maps.Map("map", {
    center: new naver.maps.LatLng(34.8026, 126.3898),
    zoom: 14,
  });

  naver.maps.Event.addListener(map, "click", function (e) {
    var latlng = e.coord;
    updateMarker(latlng);

    removeFacilityMarkers();
    clickedMarker = null;
  });
}

function searchAddressToCoordinate(address) {
  naver.maps.Service.geocode(
    {
      query: address,
    },
    function (status, response) {
      if (status === naver.maps.Service.Status.ERROR) {
        return alert("Something Wrong!");
      }
      if (response.v2.meta.totalCount === 0) {
        return alert("올바른 주소를 입력해주세요.");
      }

      var item = response.v2.addresses[0];
      var latlng = new naver.maps.LatLng(item.y, item.x);

      insertAddress(item.roadAddress, latlng);
    }
  );
}

naver.maps.onJSContentLoaded = selectMapList;

function insertAddress(address, latlng) {
  updateMarker(latlng);
  map.setCenter(latlng);
  map.setZoom(15);
  sendCoordinatesToServer(latlng.y, latlng.x);
}

function updateMarker(latlng) {
  if (circle) {
    circle.setMap(null);
  }

  if (marker) {
    marker.setMap(null);
  }

  marker = new naver.maps.Marker({
    map: map,
    position: latlng,
  });

  circle = new naver.maps.Circle({
    map: map,
    center: latlng,
    radius: 600,
    fillColor: "#4285F4",
    fillOpacity: 0.2,
    strokeColor: "#4285F4",
    strokeOpacity: 0.5,
    strokeWeight: 2,
  });

  sendCoordinatesToServer(latlng.y, latlng.x);
}

function sendCoordinatesToServer(lat, lng) {
  $.ajax({
    url: "/facility/around",
    method: "GET",
    data: {
      lat: lat,
      lng: lng,
    },
    success: function (response) {
      removeFacilityMarkers();
      $(".side-list").empty();
      if (Array.isArray(response) && response.length > 0) {
        for (var i = 0; i < response.length; i++) {
          var facility = response[i];
          var iconUrl = `../static/assets/img/${facility.type}.png`;
          var imgUrl = `../static/assets/placeImg/${facility.type}.jpg`;
          var facilityLatlng = new naver.maps.LatLng(
            facility.lat,
            facility.lng
          );
          var facilityMarker = new naver.maps.Marker({
            map: map,
            position: facilityLatlng,
            title: facility.name,
            icon: {
              url: iconUrl,
            },
          });
          facilityMarkers.push(facilityMarker);
          showMarkerDetails(facility, imgUrl);
        }
      } else {
        alert("주변에 시설이 없습니다.");
      }
    },
    error: function (request, status, error) {
      console.error("주변 시설을 불러오는 중 에러 발생", error);
      alert("주변 시설을 불러오지 못했습니다. 다시 시도해주세요.");
    },
  });
}

function removeFacilityMarkers() {
  for (var i = 0; i < facilityMarkers.length; i++) {
    facilityMarkers[i].setMap(null);
  }
  facilityMarkers = [];
}

document.addEventListener("DOMContentLoaded", function () {
  var sidebar = document.querySelector(".sidebar");
  var toggleButton = document.querySelector(".toggle-btn");

  toggleButton.addEventListener("click", function () {
    sidebar.classList.toggle("sidebar-collapsed");
    if (sidebar.classList.contains("sidebar-collapsed")) {
      toggleButton.style.left = "0px";
      toggleButton.textContent = "<";
    } else {
      toggleButton.style.left = "400px";
      toggleButton.textContent = ">";
    }
  });
  selectMapList();
});

var eduInstitude = document.getElementById("edInstitude");

function openModal() {
  var modal = document.getElementById("myModal");
  modal.style.display = "block";
}

function showMarkerDetails(place, imgUrl) {
  $(".sideBarContainer").css("display", "block");
  var html = `
  <div class="card">
    <div class="card-body">
      <div class="col-md-4">
        <img src="${imgUrl}" alt="이미지">
      </div>
      <div id="place_intro">
        <h5 class="card-title">${place.name}</h5>
        <a class="card-subtitle">${place.type}</a>
      </div>
      <p class="card-text">${place.address}</p>
    </div>
  </div>
  <hr />
`;

  // Append the HTML to the side-list container
  $(".side-list").append(html);
}

function searchByFilter() {
  const selectedDetail = $("#selected-details")[0].outerText;
  var cleanedText = selectedDetail.replace(/×/g, "");
  var resultArray = cleanedText.split("\n").filter(Boolean);
  showMarkers(resultArray);
  $("#myModal").hide();
}

function displayOnMap(arr) {
  $(".side-list").empty();
  removeFacilityMarkers();
  arr.forEach(function (item) {
    var iconUrl = `../static/assets/img/${item.type || "아파트"}.png`;
    var imgUrl = `../static/assets/placeImg/${item.type || "아파트"}.jpg`;
    var facilityMarker = new naver.maps.Marker({
      map: map,
      position: new naver.maps.LatLng(item.lat, item.lng),
      title: item.name,
      icon: {
        url: iconUrl,
      },
    });
    showMarkerDetails(item, imgUrl);
    facilityMarkers.push(facilityMarker);
  });
}

function showMarkers(keyArr) {
  var bounds = map.getBounds();
  var center = bounds.getCenter();
  removeFacilityMarkers();

  keyArr.forEach(function (key) {
    $.ajax({
      url: "/facility/",
      method: "GET",
      contentType: "application/json",
      data: {
        lat: center.lat(),
        lng: center.lng(),
        type: key,
      },
      success: function (response) {
        displayOnMap(response);
      },
      error: function (request, status, error) {
        console.error("주변 시설을 불러오는 중 에러 발생", error);
        alert("주변 시설을 불러오지 못했습니다. 다시 시도해주세요.");
      },
    });
  });
}

document.addEventListener("DOMContentLoaded", function () {
  var span = document.getElementsByClassName("close")[0];
  span.onclick = closeModal;
  var categoryColors = {
    medical: "#abf7b1",
    education: "#fcfcdc",
    facilities: "lightskyblue",
    residential: "lightcoral",
    leisure: "thistle",
  };

  document.querySelectorAll(".category").forEach(function (button) {
    button.addEventListener("click", function () {
      var category = this.getAttribute("data-category");
      var detailsId = "details-" + category;
      var arrow = document.getElementById("arrow");
      var categoryButton = document.getElementById(category);

      document.querySelectorAll(".category").forEach(function (category) {
        category.style.backgroundColor = "";
      });

      categoryButton.style.backgroundColor = categoryColors[category];

      document
        .querySelectorAll(".detail-container")
        .forEach(function (container) {
          container.style.display = "none";
        });

      var detailsContainer = document.getElementById(detailsId);
      detailsContainer.style.display = "flex";
      arrow.style.display =
        detailsContainer.style.display === "flex" ? "block" : "none";

      detailsContainer.querySelectorAll(".detail").forEach(function (detail) {
        detail.removeEventListener("click", handleDetailClick);

        detail.addEventListener("click", handleDetailClick);
      });
    });
  });

  function handleDetailClick() {
    var detailText = this.textContent.trim();
    var isDuplicate = Array.from(
      document.querySelectorAll("#selected-details .selected-detail-item")
    ).some(function (item) {
      return item.textContent.trim().indexOf(detailText) > -1;
    });
    var perfecthomes = document.getElementById("perfecthomes");
    perfecthomes.style.display = "block";

    if (!isDuplicate) {
      addSelectedDetail(
        this.textContent.trim(),
        this.parentNode.getAttribute("id").replace("details-", "")
      );
    }
  }

  function addSelectedDetail(detailText, category) {
    var detailEl = document.createElement("div");
    detailEl.classList.add("selected-detail-item");
    detailEl.textContent = detailText;
    detailEl.style.backgroundColor = categoryColors[category];
    var removeBtn = document.createElement("span");
    removeBtn.textContent = "×";
    removeBtn.onclick = function () {
      detailEl.remove();
    };
    removeBtn.style.cursor = "pointer";
    removeBtn.style.marginLeft = "10px";
    detailEl.appendChild(removeBtn);

    document.getElementById("selected-details").appendChild(detailEl);
  }

  function closeModal() {
    modal.style.display = "none";

    document.querySelectorAll(".category").forEach(function (category) {
      category.style.backgroundColor = "";
    });

    var selectedDetailsContainer = document.getElementById("selected-details");
    selectedDetailsContainer.innerHTML = "";

    var detailContainers = document.querySelectorAll(".detail-container");
    detailContainers.forEach(function (container) {
      container.style.display = "none";
    });

    var arrow = document.getElementById("arrow");
    arrow.style.display = "none";

    var perfecthomes = document.getElementById("perfecthomes");
    perfecthomes.style.display = "none";
  }
});

function handleFormSubmit(event) {
  event.preventDefault();
  // Get the input element by its ID
  var inputElement = document.getElementById("ai-txt");

  // Access the value of the input element
  var inputValue = inputElement.value;

  $.ajax({
    url: "/apartment/gpt-search",
    method: "POST",
    data: {
      question: inputValue,
    },
    success: function (response) {
      displayOnMap(response);
      /*
      removeFacilityMarkers();
      $(".side-list").empty();
      console.log("choices : ", response);
      const choices = response?.choices;
      if (choices.length > 0) {
        for (var i = 0; i < choices.length; i++) {
          var aiReturn = JSON.parse(choices[i].message.content);

          $.ajax({
            url: "/apartment/search",
            method: "POST",
            contentType: "application/json",
            data: aiReturn,
            success: function (response) {
              displayOnMap(response);
            },
            error: function (request, status, error) {
              console.error("주변 시설을 불러오는 중 에러 발생", error);
              alert("주변 시설을 불러오지 못했습니다. 다시 시도해주세요.");
            },
          });
          return;
        }
      } else {
        alert("주변에 시설이 없습니다.");
      }*/
    },
    error: function (request, status, error) {
      console.error("주변 시설을 불러오는 중 에러 발생", error);
      alert("주변 시설을 불러오지 못했습니다. 다시 시도해주세요.");
    },
  });
  // Additional logic here
}
