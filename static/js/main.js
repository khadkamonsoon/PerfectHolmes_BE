var map;
var circle;
var marker;
var facilityMarkers = [];
var clickedMarker;

var places = [
  {
    name: "나무숲",
    subtitle: "카페",
    description: "빙수개커욘",
    imageUrl:
      "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyNDAyMDhfMTU1%2FMDAxNzA3MzU1NzA0NTIz.Lfj4DJMS9bqkRRXPTXMtDf91yZTuupGt6wO-YbfN47Yg.Lq54OmwRmYGZjhhzTWf4Hm1F5esR5lmsureDZZhLrVUg.JPEG.bdsea1217%2FIMG_7409.jpg&type=f&size=680x360&quality=80&opt=2",
  },
  {
    name: "오늘은 왠지",
    subtitle: "카페",
    description: "커피맛이 너무 고급스러워요, 목대 커피는 owen",
    imageUrl:
      "https://search.pstatic.net/common/?src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20221020_229%2F1666253513669TeKUY_JPEG%2F94E54031-7DD6-4B42-AE98-5511F3224B50.jpeg",
  },
  {
    name: "메가커피",
    subtitle: "카페",
    description:
      "위치도 좋고 커피도 맛있는 이곳, 패스오더 서비스 도입되면 더 자주 방문할거같아요",
    imageUrl:
      "https://search.pstatic.net/common/?src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20210206_250%2F1612575043521ah9D6_JPEG%2FMfZhDYNAK4n0KZPidaoJgc_b.jpg",
  },
  {
    name: "나무숲",
    subtitle: "카페",
    description: "빙수개커욘",
    imageUrl:
      "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyNDAyMDhfMTU1%2FMDAxNzA3MzU1NzA0NTIz.Lfj4DJMS9bqkRRXPTXMtDf91yZTuupGt6wO-YbfN47Yg.Lq54OmwRmYGZjhhzTWf4Hm1F5esR5lmsureDZZhLrVUg.JPEG.bdsea1217%2FIMG_7409.jpg&type=f&size=680x360&quality=80&opt=2",
  },
];

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

$("#address").on("keydown", function (e) {
  var keyCode = e.which;
  if (keyCode === 13) {
    searchAddressToCoordinate($("#address").val());
  }
});

$("#submit").on("click", function (e) {
  e.preventDefault();
  console.log("test");
  searchAddressToCoordinate($("#address").val());
});

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
      if (Array.isArray(response) && response.length > 0) {
        for (var i = 0; i < response.length; i++) {
          var facility = response[i];
          var facilityLatlng = new naver.maps.LatLng(
            facility.lat,
            facility.lng
          );
          var facilityMarker = new naver.maps.Marker({
            map: map,
            position: facilityLatlng,
            title: facility.name,
          });
          facilityMarkers.push(facilityMarker);
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

var modal = document.getElementById("myModal");

var eduInstitude = document.getElementById("edInstitude");

function openModal() {
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
  $(".side-list").html(html);
}

function displayOnMap(arr, iconUrl, imgUrl) {
  arr.forEach(function (item) {
    var facilityMarker = new naver.maps.Marker({
      map: map,
      position: new naver.maps.LatLng(item.lat, item.lng),
      title: item.name,
      icon: {
        url: iconUrl,
      },
    });
    facilityMarkers.push(facilityMarker);
    facilityMarker.addListener("click", function () {
      showMarkerDetails(item, imgUrl);
    });
  });
}

function showMarkers(keyArr) {
  var bounds = map.getBounds();
  var center = bounds.getCenter();
  removeFacilityMarkers();

  keyArr.forEach(function (key) {
    console.log("key : ", key);
    const imgName = key.replaceAll(" ", "");
    var iconUrl = `../static/assets/img/${imgName}.png`;
    var imgUrl = `../static/assets/placeImg/${imgName}.jpg`;
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
        displayOnMap(response, iconUrl, imgUrl);
      },
      error: function (request, status, error) {
        console.error("주변 시설을 불러오는 중 에러 발생", error);
        alert("주변 시설을 불러오지 못했습니다. 다시 시도해주세요.");
      },
    });
  });
}

window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};

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
