provinceSelect = document.getElementById('id_province_id');
citySelect = document.getElementById('id_city_id');
provinceName = document.getElementById('id_province');
cityName = document.getElementById('id_city');
postalCodeInput = document.getElementById('id_postal_code');

const showProvinces = () => {
  const url = '/get_provinces/';

  fetch(url, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
  })
    .then((response) => {
      return response.json();
    })
    .then((provinces) => {
      provinces.forEach((province) => {
        const optionElement = document.createElement('option');
        optionElement.value = province.province_id;
        optionElement.text = province.province;

        provinceSelect.options.add(optionElement);
      });
      provinceName.value = provinces[0].province;
    });
};

showProvinces();

provinceSelect.addEventListener('change', () => {
  const text = provinceSelect.options[provinceSelect.selectedIndex].text;

  if (text === 'Pilih Provinsi') {
    const optionElement = document.createElement('option');
    optionElement.value = '';
    optionElement.text = 'Pilih Kabupaten';
    provinceName.value = '';

    citySelect.options.add(optionElement);
  } else {
    citySelect.options.length = 0;
    provinceName.value = text;
    showCities(provinceSelect.value);
  }
});

citySelect.addEventListener('change', () => {
  const text = citySelect.options[citySelect.selectedIndex].text;
  cityName.value = text;

  if (text !== 'Pilih Kabupaten / Kota') {
    setPostalCode(citySelect.value);
  }
});

const showCities = (provinceId) => {
  const url = '/get_cities/';

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    body: JSON.stringify({ provinceId }),
  })
    .then((response) => {
      return response.json();
    })
    .then((cities) => {
      cities.forEach((city) => {
        const optionElement = document.createElement('option');
        optionElement.value = city.city_id;
        optionElement.text = city.city_name;

        citySelect.options.add(optionElement);
      });
      cityName.value = cities[0].city_name;
      setPostalCode(cities[0].city_id);
    });
};

const setPostalCode = (cityId) => {
  const url = `/get_city/${cityId}/`;

  fetch(url, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
  })
    .then((response) => {
      return response.json();
    })
    .then((city) => {
      postalCodeInput.value = city.postal_code;
    });
};

// const showDistricts = (regencyId) => {
//   fetch(`http://www.emsifa.com/api-wilayah-indonesia/api/districts/${regencyId}.json`)
//     .then((response) => response.json())
//     .then((disctricts) => {
//       disctricts.forEach((district) => {
//         const optionElement = document.createElement('option');
//         optionElement.value = district.id;
//         optionElement.text = district.name;

//         districtSelect.options.add(optionElement);
//       });
//     });
// };

// const showVillages = (districtId) => {
//   fetch(`http://www.emsifa.com/api-wilayah-indonesia/api/villages/${districtId}.json`)
//     .then((response) => response.json())
//     .then((villages) => {
//       villages.forEach((village) => {
//         const optionElement = document.createElement('option');
//         optionElement.value = village.id;
//         optionElement.text = village.name;

//         villageSelect.options.add(optionElement);
//       });
//     });
// };
